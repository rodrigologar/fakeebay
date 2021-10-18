# Generated by Django 3.2.6 on 2021-10-18 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_alter_listing_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reply',
            name='comment',
        ),
        migrations.AlterField(
            model_name='listing',
            name='category',
            field=models.CharField(blank=True, choices=[('AU', 'Automotive'), ('BA', 'Babies'), ('BE', 'Beauty'), ('BO', 'Books'), ('EL', 'Electronics'), ('FA', 'Fashion'), ('HE', 'Health'), ('HO', 'Home'), ('SP', 'Sports'), ('OT', 'Other')], max_length=2),
        ),
        migrations.AlterField(
            model_name='listing',
            name='image',
            field=models.URLField(blank=True),
        ),
        migrations.DeleteModel(
            name='Bid',
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
        migrations.DeleteModel(
            name='Reply',
        ),
    ]