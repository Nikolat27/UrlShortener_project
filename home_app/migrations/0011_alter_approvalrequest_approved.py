# Generated by Django 5.1.2 on 2024-10-13 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home_app', '0010_alter_approvalrequest_approved_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='approvalrequest',
            name='approved',
            field=models.CharField(choices=[('approved', 'Approved'), ('pending', 'Pending'), ('rejected', 'Rejected')], default='sam', max_length=10),
        ),
    ]
