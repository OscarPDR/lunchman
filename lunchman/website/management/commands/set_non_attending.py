
from django.core.management.base import BaseCommand
from website.models import AttendedMeal, UserSettings

import datetime

import logging
logger = logging.getLogger(__name__)


class Command(BaseCommand):

    help = u"Sets the non-attending flag for those whose default is such"

    def handle(self, *args, **options):

        non_attending_users = UserSettings.objects.filter(default_behaviour='default_no')

        for non_attendee in non_attending_users:

            if AttendedMeal.objects.filter(person=non_attendee.user, date=datetime.date.today()).count() == 0:

                logger.info(u'Setting the non-attending default for user <%s>' % non_attendee.user.username)

                AttendedMeal.objects.create(
                    person=non_attendee.user,
                    date=datetime.date.today(),
                    preferred_time='non-attending',
                )

            else:
                logger.info(u'User <%s> already defined an action for today' % non_attendee.user.username)
