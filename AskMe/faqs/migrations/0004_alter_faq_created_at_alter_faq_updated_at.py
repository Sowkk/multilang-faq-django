# Generated by Django 5.1.5 on 2025-02-08 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('faqs', '0003_alter_faq_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='faq',
            name='created_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='faq',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
