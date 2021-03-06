# Generated by Django 2.1.15 on 2020-05-11 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('opportunities', '0009_auto_20200511_0248'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='opportunity',
            index=models.Index(fields=['title'], name='title_idx'),
        ),
        migrations.AddIndex(
            model_name='opportunity',
            index=models.Index(fields=['company'], name='company_idx'),
        ),
        migrations.AddIndex(
            model_name='opportunity',
            index=models.Index(fields=['location'], name='location_idx'),
        ),
        migrations.AddIndex(
            model_name='opportunity',
            index=models.Index(fields=['-date'], name='date_desce_idx'),
        ),
        migrations.AddIndex(
            model_name='opportunity',
            index=models.Index(fields=['jobType'], name='jobType_idx'),
        ),
    ]
