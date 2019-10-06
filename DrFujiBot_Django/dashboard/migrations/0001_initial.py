# Generated by Django 2.2.5 on 2019-09-29 13:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SimpleOutput',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('output_text', models.CharField(max_length=5000)),
            ],
        ),
        migrations.CreateModel(
            name='Command',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('command', models.CharField(max_length=200)),
                ('permissions', models.IntegerField(choices=[(1, 'Broadcaster Only'), (2, 'Moderator Only'), (3, 'Subscriber Only'), (4, 'Everyone')], default=4)),
                ('invocation_count', models.IntegerField(default=0)),
                ('is_built_in', models.BooleanField(default=False)),
                ('output', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dashboard.SimpleOutput')),
            ],
        ),
    ]
