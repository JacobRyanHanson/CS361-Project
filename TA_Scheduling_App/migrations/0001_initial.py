# Generated by Django 4.2 on 2023-05-04 23:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Course",
            fields=[
                ("COURSE_ID", models.AutoField(primary_key=True, serialize=False)),
                ("COURSE_NUMBER", models.IntegerField()),
                ("COURSE_NAME", models.CharField(max_length=255)),
                ("COURSE_DESCRIPTION", models.TextField()),
                ("SEMESTER", models.CharField(max_length=255)),
                ("PREREQUISITES", models.CharField(max_length=255, null=True)),
                ("DEPARTMENT", models.CharField(max_length=255)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="CourseAssignment",
            fields=[
                (
                    "COURSE_ASSIGNMENT_ID",
                    models.AutoField(primary_key=True, serialize=False),
                ),
                ("IS_GRADER", models.BooleanField(null=True)),
                (
                    "COURSE",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="TA_Scheduling_App.course",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Section",
            fields=[
                ("SECTION_ID", models.AutoField(primary_key=True, serialize=False)),
                ("SECTION_TYPE", models.CharField(max_length=10)),
                ("SECTION_NUMBER", models.IntegerField()),
                ("BUILDING", models.CharField(max_length=255)),
                ("ROOM_NUMBER", models.CharField(max_length=10)),
                ("SECTION_START", models.TimeField()),
                ("SECTION_END", models.TimeField()),
                (
                    "COURSE",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="TA_Scheduling_App.course",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="User",
            fields=[
                ("USER_ID", models.AutoField(primary_key=True, serialize=False)),
                ("ROLE", models.CharField(max_length=10)),
                ("FIRST_NAME", models.CharField(max_length=255)),
                ("LAST_NAME", models.CharField(max_length=255)),
                ("EMAIL", models.EmailField(max_length=254, unique=True)),
                ("PASSWORD_HASH", models.CharField(max_length=255)),
                ("PHONE_NUMBER", models.CharField(max_length=20)),
                ("ADDRESS", models.CharField(max_length=255)),
                ("BIRTH_DATE", models.DateField()),
                ("SKILLS", models.CharField(max_length=255, null=True)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="SectionAssignment",
            fields=[
                (
                    "SECTION_ASSIGNMENT_ID",
                    models.AutoField(primary_key=True, serialize=False),
                ),
                (
                    "COURSE_ASSIGNMENT",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="TA_Scheduling_App.courseassignment",
                    ),
                ),
                (
                    "SECTION",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="TA_Scheduling_App.section",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.AddField(
            model_name="courseassignment",
            name="USER",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="TA_Scheduling_App.user"
            ),
        ),
    ]
