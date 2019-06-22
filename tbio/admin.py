from django.contrib import admin

from tbio import models


admin.site.register(models.AuthUser)
admin.site.register(models.TwitterUser)

# reverse() does not work here
admin.site.site_url = '/tbio/'
