# Generated by Django 5.1.6 on 2025-03-04 10:17

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Pet",
            fields=[
                ("pet_id", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=100)),
                (
                    "sex",
                    models.CharField(
                        choices=[("Male", "Male"), ("Female", "Female")], max_length=10
                    ),
                ),
                ("age", models.IntegerField()),
                ("weight", models.FloatField()),
                ("breed", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "size",
                    models.CharField(
                        choices=[
                            ("Small", "Small"),
                            ("Medium", "Medium"),
                            ("Large", "Large"),
                        ],
                        max_length=50,
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[("Available", "Available"), ("Adopted", "Adopted")],
                        default="Available",
                        max_length=20,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "type",
                    models.CharField(
                        choices=[("Dog", "Dog"), ("Cat", "Cat")], max_length=50
                    ),
                ),
                (
                    "posted_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="PetImage",
            fields=[
                ("pet_image_id", models.AutoField(primary_key=True, serialize=False)),
                ("pet_image", models.ImageField(upload_to="pet_images/")),
                (
                    "pet",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="images",
                        to="posts.pet",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="PostPetInfo",
            fields=[
                ("post_info_id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "operator_username",
                    models.CharField(blank=True, max_length=150, null=True),
                ),
                ("home_type", models.CharField(blank=True, max_length=100, null=True)),
                ("home_ownership", models.BooleanField(default=False)),
                ("has_landlord_permission", models.BooleanField(default=False)),
                ("has_other_pets", models.BooleanField(default=False)),
                ("has_children", models.BooleanField(default=False)),
                ("experience_with_pets", models.BooleanField(default=False)),
                ("reason_for_fostering", models.TextField(blank=True, null=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("Pending", "Pending"),
                            ("Approved", "Approved"),
                            ("Rejected", "Rejected"),
                        ],
                        default="Pending",
                        max_length=20,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("pet_passport", models.BooleanField(default=False)),
                ("vaccinated", models.BooleanField(default=False)),
                (
                    "pet",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="posts.pet"
                    ),
                ),
                (
                    "username",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="posted_pets",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="PostReview",
            fields=[
                ("post_id", models.AutoField(primary_key=True, serialize=False)),
                ("date", models.DateTimeField(auto_now=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("Pending", "Pending"),
                            ("Approved", "Approved"),
                            ("Rejected", "Rejected"),
                        ],
                        default="Pending",
                        max_length=20,
                    ),
                ),
                (
                    "operator_username",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="reviewed_posts",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "pet_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="posts.pet"
                    ),
                ),
                (
                    "username",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="post_reviews",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
