# Generated by Django 2.0 on 2018-11-01 12:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('humanist_app', '0009_subscriber_digest'),
    ]

    operations = [
        migrations.AlterField(
            model_name='editedemail',
            name='incoming',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='humanist_app.IncomingEmail'),
        ),
    ]
