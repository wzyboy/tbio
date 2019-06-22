import os
import time
import glob
import json
import pickle

import twitter
from django.db import transaction
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.core.management.base import CommandError
from django.utils import timezone

from tbio.models import TwitterUser
from tbio.models import SyncRecord
from tbio.utils import cleanse_friends
from tbio.utils import get_auth_user


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('auth_user', help='auth user id or screen_name')
        parser.add_argument('--source', choices=['pickle', 'json-dir', 'api'], required=True)
        parser.add_argument('--source-path')
        parser.add_argument('--clean-up', action='store_true', help='clean up duplicate history records')

    def handle(self, *args, **kwargs):

        ts_start = time.time()

        # Look up user
        user = get_auth_user(kwargs['auth_user'])
        if not user:
            raise CommandError(f'AuthUser {kwargs["auth_user"]} not found')

        # Load friends
        if kwargs['source'] == 'pickle':
            if not kwargs['source_path']:
                raise CommandError('--source-path required')
            with open(kwargs['source_path'], 'rb') as f:
                friends = pickle.load(f)
                friends = cleanse_friends(friends)
        elif kwargs['source'] == 'json-dir':
            if not kwargs['source_path']:
                raise CommandError('--source-path required')
            json_files = glob.glob(os.path.join(kwargs['source_path'], '*.json'))
            friends = []
            for json_file in json_files:
                with open(json_file, 'r') as f:
                    friend = json.load(f)
                friends.append(friend)
        elif kwargs['source'] == 'api':
            friends = load_friends_from_api(user)
        else:
            raise NotImplementedError()

        # Create records
        with transaction.atomic():
            #TwitterUser.objects.bulk_create(entries, ignore_conflicts=True)
            for friend in friends:
                twitter_user, created = TwitterUser.objects.update_or_create(
                    id=friend['id'],
                    defaults={
                        'screen_name': friend['screen_name'],
                        'name': friend['name'] or '',
                        'location': friend['location'] or '',
                        'description': friend['description'] or '',
                        'url': friend['url'] or '',
                        '_json': friend,
                    }
                )
                user.gazing.add(twitter_user)

        # Clean up duplicate history records
        if kwargs['clean_up']:
            call_command('clean_duplicate_history', '--auto', '-m', '60', verbosity=0)

        # Create sync record
        ts_end = time.time()
        duration_s = int(ts_end - ts_start)
        sync_datetime = timezone.now()
        sync_record = SyncRecord(
            datetime=sync_datetime,
            source=kwargs['source'],
            auth_user=user,
            duration_s=duration_s,
            count=len(friends),
        )
        sync_record.save()


def load_friends_from_api(auth_user):

    api = twitter.Api(
        consumer_key=auth_user.ck,
        consumer_secret=auth_user.cs,
        access_token_key=auth_user.atk,
        access_token_secret=auth_user.ats,
    )
    friends = api.GetFriends()
    friends = cleanse_friends(friends)
    return friends
