
# coding: utf-8

from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.template import loader
from website.models import AttendedMeal

import datetime


class Command(BaseCommand):

    help = u"Send email remainder to those who have not confirmed attendance"

    def handle(self, *args, **options):

        today = datetime.date.today()

        attendee_ids = AttendedMeal.objects.filter(date=today).values_list('person__id', flat=True)
        non_attendance = User.objects.all().exclude(id__in=attendee_ids)

        for person in non_attendance:

            subject = u'%s %s, ¿Subes a comer hoy?' % (person.first_name, person.last_name)
            html_message = loader.render_to_string('attendance_remainder_email.html', {})

            send_mail(
                subject,     # Subject
                "Recuerda confirmar asistencia antes de las 12:45h",     # Message
                getattr(settings, 'SENDER_ADDRESS', ''),     # From
                [person.email],     # Recipient list
                html_message=html_message,
            )

            print 'Mail sent to %s %s' % (person.first_name, person.last_name)
