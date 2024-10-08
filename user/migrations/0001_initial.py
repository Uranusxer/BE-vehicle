# Generated by Django 5.0.6 on 2024-07-09 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, unique=True)),
                ('password', models.CharField(max_length=255)),
                ('register_time', models.FloatField(default=1720508495.787176)),
                ('login_time', models.FloatField(default=1720508495.787176)),
                ('phone', models.BigIntegerField(default=0, null=True)),
                ('status', models.CharField(choices=[('online', 'Online'), ('offline', 'Offline')], default='offline', max_length=20)),
            ],
        ),
    ]
