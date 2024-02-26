export default function Dashboard() {
  return (
    <div className="flex flex-col items-center justify-center">
      <h1 className="text-xl font-bold">Upload your audio file (.mp3) to get started.</h1>

      <input
        type="file"
        accept="audio/mp3"
        className="file-input file-input-bordered file-input-success mx-auto my-4 w-full max-w-xs"
      />
    </div>
  );
}
