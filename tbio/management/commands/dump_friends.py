import os
import json
import pickle

import twitter
from django.core.management.base import BaseCommand
from django.core.management.base import CommandError

from tbio.utils import cleanse_friends
from tbio.utils import get_auth_user


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('auth_user', help='auth user id or screen_name')
        parser.add_argument('--target', choices=['pickle', 'json-dir'], required=True)
        parser.add_argument('--target-path', required=True)

    def handle(self, *args, **kwargs):

        # Look up AuthUser
        user = get_auth_user(kwargs['auth_user'])
        if not user:
            raise CommandError(f'AuthUser {kwargs["auth_user"]} not found')

        # Fetch data from API
        api = twitter.Api(
            consumer_key=user.ck,
            consumer_secret=user.cs,
            access_token_key=user.atk,
            access_token_secret=user.ats,
        )
        friends = api.GetFriends()

        # Dump raw data to pickle
        if kwargs['target'] == 'pickle':
            with open(kwargs['target_path'], 'wb') as f:
                pickle.dump(friends, f)

        # Dump cleansed data to JSON files
        elif kwargs['target'] == 'json-dir':

            friends = cleanse_friends(friends)

            o_dir = kwargs['target_path']
            os.makedirs(o_dir, exist_ok=True)

            for friend in friends:
                pretty_json = json.dumps(friend, indent=2, ensure_ascii=False, sort_keys=True)
                o_file = os.path.join(o_dir, f'{friend["id"]}.json')
                with open(o_file, 'w') as f:
                    f.write(pretty_json)
