# Generated by Django 4.2 on 2024-05-03 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0002_alter_sales_total_price_alter_sales_transaction_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sales',
            name='transaction_id',
            field=models.CharField(blank=True, help_text='leave it blank, the code will be autogenerated', max_length=15, null=True),
        ),
    ]
