import textwrap
from ast import literal_eval

from tbio.models import AuthUser


def get_auth_user(screen_name_or_id):

    if screen_name_or_id.isdigit():
        user_id = int(screen_name_or_id)
        try:
            user = AuthUser.objects.get(id=user_id)
        except AuthUser.DoesNotExist:
            return None
    else:
        user_screen_name = screen_name_or_id
        try:
            user = AuthUser.objects.get(screen_name=user_screen_name)
        except AuthUser.DoesNotExist:
            return None

    return user


def cleanse_friends(friends):

    cleansed_friends = []

    for friend in friends:
        _json = friend._json

        # Remove the latest tweet
        try:
            del _json['status']
        except KeyError:
            pass

        # Expand t.co URLs
        entities = _json.get('entities', {})
        for entity_type in ('url', 'description'):
            url_dicts = entities.get(entity_type, {}).get('urls', [])
            for url_dict in url_dicts:
                if url_dict['expanded_url']:
                    _json[entity_type] = _json[entity_type].replace(
                        url_dict['url'], url_dict['expanded_url']
                    )

        # Remove entities
        del _json['entities']

        cleansed_friends.append(_json)

    return cleansed_friends


def make_list_of_strings(user):

    text = textwrap.dedent(f'''\
        name: {user.name}
        screen_name: @{user.screen_name}
        location: {user.location}
        url: {user.url}
        description: ''')

    # user.description may contain newlines
    text += user.description
    lines = text.splitlines()

    return lines


def get_user_details(user):

    return literal_eval(user._json)
