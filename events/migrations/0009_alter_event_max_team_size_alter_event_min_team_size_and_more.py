# Generated by Django 4.1.1 on 2022-11-14 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0008_alter_teammembers_unique_together"),
    ]

    operations = [
        migrations.AlterField(
            model_name="event",
            name="max_team_size",
            field=models.IntegerField(default=1, editable=False),
        ),
        migrations.AlterField(
            model_name="event",
            name="min_team_size",
            field=models.IntegerField(default=1, editable=False),
        ),
        migrations.AlterField(
            model_name="event",
            name="type",
            field=models.CharField(
                choices=[("INDIVIDUAL", "individual event"), ("TEAM", "team event")],
                default="INDIVIDUAL",
                editable=False,
                max_length=15,
            ),
        ),
    ]
