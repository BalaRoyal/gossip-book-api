# Generated by Django 3.0.7 on 2020-07-18 13:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('utils', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('basegossipquestionmodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='utils.BaseGossipQuestionModel')),
            ],
            bases=('utils.basegossipquestionmodel', models.Model),
        ),
    ]
