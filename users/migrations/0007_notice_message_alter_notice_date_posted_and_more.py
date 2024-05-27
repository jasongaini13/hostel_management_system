# Generated by Django 5.0.6 on 2024-05-24 04:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_notice'),
    ]

    operations = [
        migrations.AddField(
            model_name='notice',
            name='message',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='notice',
            name='date_posted',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='notice',
            name='subject',
            field=models.CharField(max_length=255),
        ),
    ]