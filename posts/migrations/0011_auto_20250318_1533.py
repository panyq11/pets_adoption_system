# Generated by Django 2.1.5 on 2025-03-18 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0010_postpetinfo_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='petimage',
            name='pet_image',
            field=models.ImageField(blank=True, null=True, upload_to='pet_images/'),
        ),
    ]
