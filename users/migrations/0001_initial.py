# Generated by Django 4.1.7 on 2023-02-15 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=100)),
                ('realname', models.CharField(max_length=100)),
                ('created_at', models.DateField(auto_now_add=True)),
            ],
            options={
                'db_table': 'users',
            },
        ),
    ]
