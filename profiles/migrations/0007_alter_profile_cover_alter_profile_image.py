# Generated by Django 4.2.5 on 2023-09-30 08:14

from django.db import migrations
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0006_profile_tagline'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='cover',
            field=sorl.thumbnail.fields.ImageField(default='1', upload_to='profiles'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=sorl.thumbnail.fields.ImageField(default='1', upload_to='profiles'),
        ),
    ]
