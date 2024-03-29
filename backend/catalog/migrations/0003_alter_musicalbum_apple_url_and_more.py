# Generated by Django 4.2.5 on 2023-09-29 23:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_musicalbum_yandex_url_alter_musicalbum_wiki_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='musicalbum',
            name='apple_url',
            field=models.URLField(blank=True, null=True, verbose_name='Apple Music'),
        ),
        migrations.AlterField(
            model_name='musicalbum',
            name='spotify_url',
            field=models.URLField(blank=True, null=True, verbose_name='Spotify'),
        ),
        migrations.AlterField(
            model_name='musicalbum',
            name='wiki_url',
            field=models.URLField(blank=True, null=True, verbose_name='Wikipedia'),
        ),
        migrations.AlterField(
            model_name='musicalbum',
            name='yandex_url',
            field=models.URLField(blank=True, null=True, verbose_name='Yandex Music'),
        ),
        migrations.AlterField(
            model_name='musicalbum',
            name='youtube_url',
            field=models.URLField(blank=True, null=True, verbose_name='YouTube'),
        ),
    ]
