# Generated by Django 3.1.3 on 2021-07-12 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='question',
            old_name='contents',
            new_name='content',
        ),
        migrations.AlterField(
            model_name='answer',
            name='create_date',
            field=models.DateTimeField(),
        ),
    ]