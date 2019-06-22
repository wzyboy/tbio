from django.db import models
from simple_history.models import HistoricalRecords


class TwitterUser(models.Model):

    id = models.BigIntegerField(primary_key=True)
    screen_name = models.CharField(max_length=256)
    name = models.CharField(max_length=256, blank=True)
    location = models.CharField(max_length=256, blank=True)
    description = models.CharField(max_length=1024, blank=True)
    url = models.CharField(max_length=1024, blank=True)
    _json = models.TextField(blank=True)
    history = HistoricalRecords(
        table_name='tbio_twitter_user_history',
        custom_model_name=lambda x: f'{x}History',
        excluded_fields=['_json'],
    )

    class Meta:
        db_table = 'tbio_twitter_user'

    def __str__(self):
        return f'<User {self.screen_name} ({self.id})>'


class AuthUser(models.Model):

    id = models.BigIntegerField(primary_key=True)
    screen_name = models.CharField(max_length=128)
    ck = models.CharField(max_length=128)
    cs = models.CharField(max_length=128)
    atk = models.CharField(max_length=128)
    ats = models.CharField(max_length=128)
    gazing = models.ManyToManyField(TwitterUser, blank=True)

    class Meta:
        db_table = 'tbio_auth_user'

    def __str__(self):
        return f'<User {self.screen_name} ({self.id})>'


class SyncRecord(models.Model):

    id = models.AutoField(primary_key=True)
    datetime = models.DateTimeField()
    source = models.CharField(max_length=32)
    auth_user = models.ForeignKey(AuthUser, on_delete=models.CASCADE)
    duration_s = models.IntegerField()
    count = models.IntegerField()

    class Meta:
        db_table = 'tbio_sync_record'
