# Generated by Django 5.1.7 on 2025-03-22 03:40

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("events", "0002_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="eventnotificationconfig",
            name="reminder_mail_sent",
            field=models.BooleanField(
                default=False,
                help_text="reminder mail sent",
                verbose_name="reminder mail sent",
            ),
        ),
        migrations.AlterField(
            model_name="event",
            name="category",
            field=models.CharField(
                choices=[
                    ("music", "Music"),
                    ("nightlife", "Nightlife"),
                    ("concert", "Concert"),
                    ("holidays", "Holidays"),
                    ("dating", "Dating"),
                    ("hobbies", "Hobbies"),
                    ("coding", "Coding"),
                    ("others", "Others"),
                    ("business", "Business"),
                    ("food_drink", "Food & Drink"),
                ],
                help_text="Category",
                max_length=50,
                verbose_name="category",
            ),
        ),
        migrations.AlterField(
            model_name="event",
            name="latitude",
            field=models.DecimalField(
                blank=True, decimal_places=5, max_digits=9, null=True
            ),
        ),
        migrations.AlterField(
            model_name="event",
            name="longitude",
            field=models.DecimalField(
                blank=True, decimal_places=5, max_digits=9, null=True
            ),
        ),
        migrations.AlterField(
            model_name="event",
            name="status",
            field=models.CharField(
                choices=[
                    ("draft", "Draft"),
                    ("published", "Published"),
                    ("canceled", "Canceled"),
                ],
                help_text="Status",
                max_length=255,
                verbose_name="status",
            ),
        ),
    ]
