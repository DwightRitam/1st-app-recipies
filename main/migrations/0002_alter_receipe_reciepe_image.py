# Generated by Django 4.2.3 on 2023-07-07 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='receipe',
            name='reciepe_image',
            field=models.ImageField(upload_to='receipe/'),
        ),
    ]
