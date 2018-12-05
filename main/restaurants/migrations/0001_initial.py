# Generated by Django 2.1.4 on 2018-12-04 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Restaurants',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('type', models.CharField(max_length=200)),
                ('phone_number', models.CharField(max_length=8)),
                ('location', models.CharField(max_length=30)),
                ('address', models.CharField(max_length=200)),
            ],
        ),
    ]
