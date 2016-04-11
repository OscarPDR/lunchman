
# coding: utf-8

from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.template import loader
from website.models import AttendedMeal

import datetime

import logging
logger = logging.getLogger(__name__)


class Command(BaseCommand):

    help = u"Send email reminder to those who have not confirmed attendance"

    def handle(self, *args, **options):

        today = datetime.date.today()

        confirmed_person_ids = AttendedMeal.objects.filter(date=today).values_list('person__id', flat=True)
        non_confirmed_attendance = User.objects.all().exclude(id__in=confirmed_person_ids).exclude(username='admin')

        for person in non_confirmed_attendance:

            logger.info('Preparing lunch attendance reminder to user <%s>' % person.username)

            text_message = u'Recuerda confirmar antes de las 12:45h'

            html_message = loader.render_to_string('mail/attendance_reminder.html', {
                'full_name': u'%s %s' % (person.first_name, person.last_name),
            })

            try:
                send_mail(
                    u'[lunchman] ¿Subes a comer hoy?',
                    text_message,
                    getattr(settings, 'SENDER_ADDRESS', ''),
                    [person.email],
                    html_message=html_message,
                )

                logger.info(u'\tEmail sent')

            except:
                logger.error(u'Unable to send email to username <%s>' % person.username)
