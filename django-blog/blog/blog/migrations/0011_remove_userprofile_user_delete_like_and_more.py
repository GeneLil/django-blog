# Generated by Django 5.0.4 on 2024-07-15 20:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0010_remove_post_author_remove_post_liked_by_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="userprofile",
            name="user",
        ),
        migrations.DeleteModel(
            name="Like",
        ),
        migrations.DeleteModel(
            name="UserProfile",
        ),
    ]
