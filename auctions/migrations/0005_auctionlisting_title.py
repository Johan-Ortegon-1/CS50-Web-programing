# Generated by Django 3.2.5 on 2022-01-19 03:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_auto_20220118_1941'),
    ]

    operations = [
        migrations.AddField(
            model_name='auctionlisting',
            name='title',
            field=models.CharField(max_length=80, null=True),
        ),
    ]
