# Generated by Django 5.0.2 on 2024-02-15 22:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('audioclip', '0003_audioclip_transcription'),
    ]

    operations = [
        migrations.AlterField(
            model_name='audioclip',
            name='transcription',
            field=models.JSONField(blank=True, default=dict, null=True),
        ),
    ]
