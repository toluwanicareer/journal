# Generated by Django 2.1.3 on 2018-12-18 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pdf_converter', '0002_auto_20181218_1330'),
    ]

    operations = [
        migrations.AlterField(
            model_name='token',
            name='token',
            field=models.TextField(),
        ),
    ]
