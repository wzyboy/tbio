from django.core.management.base import BaseCommand
from requests_oauthlib import OAuth1Session


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--ck', help='CONSUMER_KEY', required=True)
        parser.add_argument('--cs', help='CONSUMER_SECRET', required=True)

    def handle(self, *args, **kwargs):

        REQUEST_TOKEN_URL = 'https://api.twitter.com/oauth/request_token'
        ACCESS_TOKEN_URL = 'https://api.twitter.com/oauth/access_token'
        AUTHORIZATION_URL = 'https://api.twitter.com/oauth/authorize'

        consumer_key = kwargs['ck']
        consumer_secret = kwargs['cs']

        oauth_client = OAuth1Session(consumer_key, client_secret=consumer_secret, callback_uri='oob')
        resp = oauth_client.fetch_request_token(REQUEST_TOKEN_URL)
        url = oauth_client.authorization_url(AUTHORIZATION_URL)
        print(f'Visit: {url}')
        pincode = input('Enter your pincode? ')

        oauth_client = OAuth1Session(
            consumer_key, client_secret=consumer_secret,
            resource_owner_key=resp.get('oauth_token'),
            resource_owner_secret=resp.get('oauth_token_secret'),
            verifier=pincode
        )
        token = oauth_client.fetch_access_token(ACCESS_TOKEN_URL)

        for k, v in token.items():
            print(f'{k}: {v}')
