# Generated by Django 5.0.6 on 2024-07-18 20:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('FinanceTracker', '0005_alter_goal_income_alter_goal_save_alter_goal_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='goal',
            old_name='save',
            new_name='saving',
        ),
    ]