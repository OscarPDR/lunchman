
from django.conf.urls import include, url
from django.contrib import admin


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', 'website.views.home', name='home'),

    # url(r'^$', 'django.contrib.auth.views.login', {'template_name': 'index.html', 'authentication_form': LoginForm}, name='home'),
    url(r'^logout/$', 'website.views.logout_view', name='logout_view'),

    url(r'^ordinary_attendance/$', 'website.views.ordinary_attendance', name='ordinary_attendance'),
    url(r'^delay_attendance/$', 'website.views.delay_attendance', name='delay_attendance'),
    url(r'^cancel_attendance/$', 'website.views.cancel_attendance', name='cancel_attendance'),

    url(r'^new_meal_ticket/$', 'website.views.new_meal_ticket', name='new_meal_ticket'),
]
