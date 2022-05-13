import tabulate
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views import View
from django.db.models import Q
from pygments.formatters import HtmlFormatter

from tbio.models import SyncRecord
from tbio.models import TwitterUser
from tbio.core.diff import get_snapshots
from tbio.core.diff import get_diff_html
from tbio.utils import get_user_details


class SyncView(View):

    def get(self, request):

        sync_records_limit = 25
        sync_records_total = SyncRecord.objects.all().count()
        sync_records = SyncRecord.objects.all().order_by('-datetime')[:sync_records_limit]
        table = [
            [row.datetime.replace(microsecond=0), row.source, row.auth_user.screen_name, row.duration_s, row.count]
            for row in sync_records
        ]
        headers = ['datetime', 'source', 'screen_name', 'duration', 'count']
        table_html = tabulate.tabulate(table, headers, tablefmt='html')

        context = {
            'sync_records_limit': sync_records_limit,
            'sync_records_total': sync_records_total,
            'table_html': table_html,
        }

        return render(request, 'sync.html', context=context)


class RecentView(View):

    def get(self, request):

        recent_changes_limit = 25
        records = (
            TwitterUser.history
            .filter(history_type='~')
            .order_by('-history_date')
            [:recent_changes_limit]
        )
        previous_records = [r.prev_record for r in records]
        deltas = [new.diff_against(old, excluded_fields=['_json']) for new, old in zip(records, previous_records)]
        recent_changes = []
        for record, delta in zip(records, deltas):
            fields = ', '.join(c.field for c in delta.changes)
            d = {
                'change_date': record.history_date.replace(microsecond=0),
                'screen_name': record.screen_name,
                'fields': fields,
            }
            recent_changes.append(d)

        context = {
            'recent_changes': recent_changes,
            'recent_changes_limit': recent_changes_limit,
        }
        return render(request, 'recent.html', context=context)


class UserView(View):

    def get(self, request, screen_name):

        user = get_object_or_404(TwitterUser, screen_name=screen_name)
        user_details = get_user_details(user)
        snapshots = get_snapshots(user.id)
        diff_css = HtmlFormatter().get_style_defs('.highlight')
        diff_html = get_diff_html(snapshots)

        context = {
            'user': user,
            'user_details': user_details,
            'diff_css': diff_css,
            'diff_html': diff_html,
        }

        return render(request, 'user.html', context=context)


class SearchView(View):

    def get(self, request):

        keyword = self.request.GET.get('q', '')
        if keyword:
            users = TwitterUser.objects.filter(
                Q(name__icontains=keyword)
                | Q(screen_name__icontains=keyword)
                | Q(location__icontains=keyword)
                | Q(url__icontains=keyword)
                | Q(description__icontains=keyword)
            )[:100]
        else:
            users = []

        context = {
            'keyword': keyword,
            'users': users,
        }

        return render(request, 'search.html', context=context)


class IndexView(View):

    def get(self, request):

        return render(request, 'index.html')
