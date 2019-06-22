# TBIO - Twitter Bio

## Installation

A MySQL server is required. You may use SQLite if you know what you are
doing. Check `settings.py` for database connection parameters.

For development (DEBUG=True):

```bash
$ python3 -m venv venv
$ source venv/bin/activate
$ (venv) pip install -r requirements.txt
$ (venv) ./manage.py migrate
$ (venv) ./manage.py runserver
```

For production deployment, use uWSGI and Nginx instead (DEBUG=False):

```bash
$ (venv) pip install -r uwsgi
$ (venv) ./manage.py collectstatic
$ (venv) uwsgi uwsgi.ini
```

```nginx
location /tbio {
  proxy_pass http://127.0.0.1:3026;
}
```

## Setup

1. Run `./manage.py createsuperuser`;
2. Visit http://locahost:3027/ and click "admin" link;
3. Log in with the superuser credentials;
4. Create an "AuthUser" with proper [Twitter API tokens](https://developer.twitter.com/en/apps);
5. Set up a cron job for `./manage.py load_friends`.
