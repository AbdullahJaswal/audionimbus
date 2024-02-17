import json
import os
import time
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path

import boto3
import psycopg2
from botocore.config import Config

print("Loading function")

my_config = Config(
    region_name="ap-southeast-2",
)

s3 = boto3.client("s3", config=my_config)
transcribe = boto3.client("transcribe", config=my_config)


def get_ai_prompts(transcription: str) -> list[dict]:
    prompt = f"""
    This is SRT subtitles of an audio:

    ---
    {transcription}
    ---

    What is the author talking about? Write detailed prompts that can be fed into an AI image generator based on the text given along with time frames in the following JSON format:

    [
        {{
            "start": "<START_TIMEFRAME>",
            "end": "<END_TIMEFRAME>",
            "prompt": "<PROMPT>"
        }},
        {{
            "start": "<START_TIMEFRAME>",
            "end": "<END_TIMEFRAME>",
            "prompt": "<PROMPT>"
        }},
    ]

    Decide the time frame ranges by yourself based on what is being talked about. Should be sequential!
    """

    headers = {
        "Content-Type": "application/json",
        "OpenAI-Organization": os.environ.get("OPENAI_ORGANIZATION"),
        "Authorization": f"Bearer {os.environ.get('OPENAI_AUTHORIZATION')}",
    }

    response = []

    try:
        url = "https://api.openai.com/v1/chat/completions"

        message = {
            "model": os.environ.get("OPENAI_MODEL"),
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 1,
        }

        data = json.dumps(message).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers=headers, method="POST")

        with urllib.request.urlopen(req) as r:
            response_body = r.read().decode("utf-8")
            gpt_response_json = json.loads(response_body)

            if "choices" in gpt_response_json and gpt_response_json["choices"]:
                gpt_response = gpt_response_json["choices"][0]["message"].get("content")
                print(gpt_response)

                if gpt_response:
                    gpt_response = gpt_response.replace("```json", "").replace(
                        "```", ""
                    )
                    gpt_response_json = json.loads(gpt_response)
                    print(json.dumps(gpt_response_json, indent=4))

                    for grj in gpt_response_json:
                        response.append(
                            {
                                "start": grj.get("start"),
                                "end": grj.get("end"),
                                "prompt": grj.get("prompt"),
                            }
                        )
    except Exception as e:
        print(f"OPENAI ERROR: {e}")

    return response


def lambda_handler(event, context):
    datetime_now = datetime.now().isoformat()
    print(f"Received Event At: {datetime_now}")

    bucket = event["Records"][0]["s3"]["bucket"]["name"]
    key = urllib.parse.unquote_plus(
        event["Records"][0]["s3"]["object"]["key"], encoding="utf-8"
    )

    file_path = Path(key.replace("audios/", ""))

    file_directory = file_path.parent
    file_name = file_path.name
    s3_uri = f"s3://audio-nimbus-initial-store/{key}"

    result = ""

    try:
        print(f"CONTENT DIR: {file_directory}")
        print(f"CONTENT NAME: {file_name}")
        print(f"JOB NAME: {file_name}")
        print(f"S3 URI: {s3_uri}")

        transcribe.start_transcription_job(
            TranscriptionJobName=file_name,
            Media={"MediaFileUri": s3_uri},
            MediaFormat="mp3",
            IdentifyLanguage=True,
            IdentifyMultipleLanguages=False,
            LanguageOptions=["en-AU", "en-GB", "en-US"],
            Subtitles={"Formats": ["srt"], "OutputStartIndex": 0},
        )

        while True:
            result = transcribe.get_transcription_job(TranscriptionJobName=file_name)

            if result["TranscriptionJob"]["TranscriptionJobStatus"] in [
                "COMPLETED",
                "FAILED",
            ]:
                break

            print("Transcribing Audio...")
            time.sleep(10)

        if result["TranscriptionJob"]["TranscriptionJobStatus"] == "COMPLETED":
            for uri in result["TranscriptionJob"]["Subtitles"]["SubtitleFileUris"]:
                with urllib.request.urlopen(uri) as response:
                    result = response.read().decode("utf-8")

                    conn = None

                    try:
                        conn = psycopg2.connect(
                            database=os.environ.get("DB_NAME"),
                            user=os.environ.get("DB_USER"),
                            password=os.environ.get("DB_PASS"),
                            host=os.environ.get("DB_HOST"),
                            port=os.environ.get("DB_PORT"),
                        )
                        query = conn.cursor()

                        query.execute(
                            """
                            UPDATE audioclip_audioclip
                            SET transcription = %s,
                                is_transcribed = %s,
                                transcribed_at = %s
                            WHERE uid = %s;
                            """,
                            (
                                result,
                                True,
                                datetime.now(),
                                file_name.replace(".mp3", ""),
                            ),
                        )
                        print("Transcription Updated")

                        print("Getting AI Prompts...")
                        ai_prompts = get_ai_prompts(result)
                        print("Received AI Prompts")

                        if ai_prompts:
                            query.execute(
                                """
                                UPDATE audioclip_audioclip
                                SET ai_prompts = %s,
                                    is_processed = %s,
                                    processed_at = %s
                                WHERE uid = %s;
                                """,
                                (
                                    json.dumps(ai_prompts, indent=4),
                                    True,
                                    datetime.now(),
                                    file_name.replace(".mp3", ""),
                                ),
                            )
                            print("AI Prompts Updated")
                    except Exception as e:
                        print(e)

                        return False
                    finally:
                        if conn is not None:
                            conn.commit()
                            conn.close()
    except Exception as err:
        print(err)
        print(
            f"Error getting object {key} from bucket {bucket}. Make sure they exist and your bucket is in the same region as this function."
        )
        return False

    return True
