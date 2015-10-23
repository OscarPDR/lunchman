
from django.conf.urls import include, url
from django.contrib import admin

import debug_toolbar


urlpatterns = [
    url(r'^__debug__/', include(debug_toolbar.urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^logout/$', 'website.views.logout_view', name='logout_view'),

    url(r'^$', 'website.views.home', name='home'),

    url(r'^settings/$', 'website.views.user_settings', name='user_settings'),

    url(r'^attendance/(?P<action>\S+)/$', 'website.views.update_attendance', name='update_attendance'),
    url(r'^attendance/$', 'website.views.update_attendance', name='update_attendance_def'),

    url(r'^attendance_ajax/$', 'website.views.update_attendance_ajax', name='update_attendance_ajax'),

    url(r'^new_meal_ticket/$', 'website.views.new_meal_ticket', name='new_meal_ticket'),
]
