# Generated by Django 2.1.3 on 2018-12-18 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pdf_converter', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Token',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=200)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.DeleteModel(
            name='File',
        ),
    ]
