# Generated by Django 4.2 on 2024-10-01 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='stockmovement',
            options={'ordering': ['-date_created'], 'verbose_name_plural': 'Stock Movement'},
        ),
        migrations.AlterField(
            model_name='order',
            name='ordered',
            field=models.BooleanField(default=False, help_text='Tick the checkbox if ordered'),
        ),
        migrations.AlterField(
            model_name='order',
            name='slug',
            field=models.SlugField(blank=True, help_text='Leave this field blank; it will be             automatically generated for you.', null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(blank=True, help_text='Leave this field blank; it will be             automatically generated for you.', null=True),
        ),
        migrations.AlterField(
            model_name='refund',
            name='accepted',
            field=models.BooleanField(default=False, help_text='Tick the checkbox if accepted'),
        ),
        migrations.AlterField(
            model_name='stock',
            name='in_stock',
            field=models.BooleanField(default=False, help_text='Tick the checkbox if the item is in stock'),
        ),
        migrations.AlterField(
            model_name='stock',
            name='stock_level',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='stockmovement',
            name='slug',
            field=models.SlugField(blank=True, help_text='Leave this field blank; it will be             automatically generated for you.', null=True),
        ),
        migrations.AlterField(
            model_name='supplier',
            name='slug',
            field=models.SlugField(blank=True, help_text='Leave this field blank; it will be             automatically generated for you.', null=True),
        ),
    ]
