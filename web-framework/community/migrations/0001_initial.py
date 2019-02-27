# Generated by Django 2.1.7 on 2019-02-22 06:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='board',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('image', models.ImageField(blank=True, upload_to='')),
                ('title', models.CharField(max_length=200)),
                ('date', models.DateField()),
                ('category', models.CharField(max_length=100)),
                ('place', models.CharField(max_length=200)),
                ('entry', models.IntegerField()),
                ('intro', models.CharField(max_length=300)),
                ('user', models.CharField(max_length=20)),
            ],
        ),
    ]
