# Generated by Django 3.2.7 on 2021-11-11 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Custom_Settings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count_pagination', models.PositiveSmallIntegerField(default=3, verbose_name='Значение пагинации')),
            ],
        ),
    ]
