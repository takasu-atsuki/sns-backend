# Generated by Django 4.1.7 on 2023-02-28 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_diary_message'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='dmail',
            unique_together=set(),
        ),
        migrations.AlterField(
            model_name='diary',
            name='message',
            field=models.CharField(blank=True, max_length=30),
        ),
    ]