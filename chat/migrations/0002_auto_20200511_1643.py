# Generated by Django 2.1.15 on 2020-05-11 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='chatmessage',
            index=models.Index(fields=['thread'], name='thread_idx'),
        ),
        migrations.AddIndex(
            model_name='chatmessage',
            index=models.Index(fields=['-timestamp'], name='time_desc_idx'),
        ),
        migrations.AddIndex(
            model_name='thread',
            index=models.Index(fields=['first'], name='thread_first_idx'),
        ),
        migrations.AddIndex(
            model_name='thread',
            index=models.Index(fields=['second'], name='thread_second_idx'),
        ),
        migrations.AddIndex(
            model_name='thread',
            index=models.Index(fields=['-timestamp'], name='thread_time_desc_idx'),
        ),
    ]
