# Generated by Django 5.1.4 on 2024-12-27 04:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_bids_comments_listings'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listings',
            name='bid',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='listing', to='auctions.bids'),
        ),
        migrations.AlterField(
            model_name='listings',
            name='comment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='listing', to='auctions.comments'),
        ),
    ]
