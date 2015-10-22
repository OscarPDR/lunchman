
# coding: utf-8

from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.template import loader
from website.models import AttendedMeal, MealTicket

import datetime

import logging
logger = logging.getLogger(__name__)


class Command(BaseCommand):

    help = u"Send reminder mail to people nearly out of meal tickets"

    def handle(self, *args, **options):

        today = datetime.date.today()

        attendee_ids = AttendedMeal.objects.filter(date=today).exclude(preferred_time='non-attending').values_list('person__id', flat=True)

        for person_id in attendee_ids:

            person = User.objects.get(pk=person_id)

            lesser_meal_ticket = MealTicket.objects.filter(owner=person, remaining_meals__gt=0).order_by('remaining_meals').first()

            if (lesser_meal_ticket) and (lesser_meal_ticket.remaining_meals < 2):

                logger.info('Preparing out-of-tickets reminder to user <%s>' % person.username)

                text_message = u'Estás casi sin tickets de comida'

                html_message = loader.render_to_string('mail/ticket_reminder.html', {
                    'full_name': u'%s %s' % (person.first_name, person.last_name),
                    'remaining_meals': lesser_meal_ticket.remaining_meals,
                })

                try:
                    send_mail(
                        u'[lunchman] Recuerda adquirir un nuevo ticket',
                        text_message,
                        getattr(settings, 'SENDER_ADDRESS', ''),
                        [person.email],
                        html_message=html_message,
                    )

                    logger.info(u'\tEmail sent')

                except:
                    logger.error(u'Unable to send email to username <%s>' % person.username)
