# Generated by Django 4.1.1 on 2022-11-02 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="event",
            name="latitude",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="event",
            name="longitude",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="event",
            name="subtype",
            field=models.CharField(
                choices=[("DANCE", "dance event")], default="DANCE", max_length=15
            ),
        ),
        migrations.AlterField(
            model_name="event",
            name="image_url",
            field=models.ImageField(upload_to=""),
        ),
    ]