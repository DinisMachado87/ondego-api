# Generated by Django 3.2.25 on 2024-04-10 01:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event_image',
            field=models.ImageField(
                blank=True, default='../ondego_event_placeholder/fhq6qy9kir3aw2ngkvlt', upload_to='ondego_events/'),
        ),
    ]
