# Generated by Django 2.2.2 on 2019-06-18 08:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AuthUser',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('screen_name', models.CharField(max_length=128)),
                ('ck', models.CharField(max_length=128)),
                ('cs', models.CharField(max_length=128)),
                ('atk', models.CharField(max_length=128)),
                ('ats', models.CharField(max_length=128)),
            ],
            options={
                'db_table': 'tbio_auth_user',
            },
        ),
        migrations.CreateModel(
            name='TwitterUser',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('screen_name', models.CharField(max_length=256)),
                ('name', models.CharField(blank=True, max_length=256)),
                ('location', models.CharField(blank=True, max_length=256)),
                ('description', models.CharField(blank=True, max_length=1024)),
                ('url', models.CharField(blank=True, max_length=1024)),
                ('_json', models.TextField(blank=True)),
            ],
            options={
                'db_table': 'tbio_twitter_user',
            },
        ),
        migrations.CreateModel(
            name='TwitterUserHistory',
            fields=[
                ('id', models.BigIntegerField(db_index=True)),
                ('screen_name', models.CharField(max_length=256)),
                ('name', models.CharField(blank=True, max_length=256)),
                ('location', models.CharField(blank=True, max_length=256)),
                ('description', models.CharField(blank=True, max_length=1024)),
                ('url', models.CharField(blank=True, max_length=1024)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical twitter user',
                'db_table': 'tbio_twitter_user_history',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='SyncRecord',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('datetime', models.DateTimeField()),
                ('source', models.CharField(max_length=32)),
                ('duration_s', models.IntegerField()),
                ('count', models.IntegerField()),
                ('auth_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tbio.AuthUser')),
            ],
            options={
                'db_table': 'tbio_sync_record',
            },
        ),
        migrations.AddField(
            model_name='authuser',
            name='gazing',
            field=models.ManyToManyField(blank=True, to='tbio.TwitterUser'),
        ),
    ]