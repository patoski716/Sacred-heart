# Generated by Django 4.2.7 on 2023-12-17 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_rename_level_payment_student_class_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='student_class',
            field=models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], default='Basic 1', max_length=100),
        ),
    ]
