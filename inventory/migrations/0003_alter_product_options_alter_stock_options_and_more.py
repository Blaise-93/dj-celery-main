# Generated by Django 4.2 on 2024-10-01 14:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_alter_stockmovement_options_alter_order_ordered_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['-date_created']},
        ),
        migrations.AlterModelOptions(
            name='stock',
            options={'ordering': ['-date_created']},
        ),
        migrations.AlterModelOptions(
            name='supplier',
            options={'ordering': ['-date_created']},
        ),
    ]
