# Generated by Django 5.0.4 on 2024-05-14 22:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_alter_post_modified_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='modified_at',
            field=models.DateTimeField(null=True),
        ),
    ]
