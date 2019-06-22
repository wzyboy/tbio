import difflib

from pygments import highlight
from pygments.lexers import DiffLexer
from pygments.formatters import HtmlFormatter
from django.contrib.humanize.templatetags import humanize

from tbio.models import TwitterUser
from tbio.utils import make_list_of_strings


def get_snapshots(user_id, max_depth=None):

    user = TwitterUser.objects.get(id=user_id)
    snapshots = []

    # Iterate from the newest to the oldest
    current = user.history.first()
    depth = 0
    while True:
        if max_depth is not None and depth >= max_depth:
            break
        text = make_list_of_strings(current.instance)
        datetime = current.history_date
        snapshots.append((datetime, text))
        if current.prev_record:
            current = current.prev_record
        else:  # end of history
            break

    return snapshots


def get_diff_html(snapshots):

    html = ''
    for new, old in zip(snapshots, snapshots[1:]):
        old_date = '{} ({})'.format(old[0].replace(microsecond=0), humanize.naturaltime(old[0]))
        new_date = '{} ({})'.format(new[0].replace(microsecond=0), humanize.naturaltime(new[0]))
        diff_text = '\n'.join(
            difflib.unified_diff(
                old[1], new[1],
                fromfiledate=old_date,
                tofiledate=new_date,
                n=5,
                lineterm='',
            )
        )
        html += highlight(diff_text, DiffLexer(), HtmlFormatter())

    return html
