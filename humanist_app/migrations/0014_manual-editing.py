# Generated by Django 2.0 on 2018-12-17 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('humanist_app', '0013_auto_20181101_1741'),
    ]

    operations = [
        migrations.AddField(
            model_name='editedemail',
            name='order_no',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='edition',
            name='manual_edit',
            field=models.BooleanField(default=False),
        ),
    ]