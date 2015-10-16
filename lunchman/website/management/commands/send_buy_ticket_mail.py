
# coding: utf-8

from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from website.models import AttendedMeal, MealTicket

import datetime


class Command(BaseCommand):

    help = u"Send remainder mail to people nearly out of meal tickets"

    def handle(self, *args, **options):

        today = datetime.date.today()

        attendee_ids = AttendedMeal.objects.filter(date=today).exclude(preferred_time='non-attending').values_list('person__id', flat=True)

        for person_id in attendee_ids:

            lesser_meal_ticket = MealTicket.objects.filter(owner=person_id, remaining_meals__gt=0).order_by('remaining_meals').first()

            if lesser_meal_ticket.remaining_meals < 2:

                person = User.objects.get(pk=person_id)

                msg = """
                    Te quedan %(remaining)d servicios restantes en tu ticket del comedor.
                    Adquiere un nuevo ticket y añadelo al saldo de tu cuenta en el menú
                    desplegable de la esquina superior derecha de la aplicación de gestión.
                """ % {'remaining': lesser_meal_ticket.remaining_meals}

                send_mail(
                    'Estás casi sin tickets de comida',     # Subject
                    msg,     # Message
                    getattr(settings, 'SENDER_ADDRESS', ''),     # From
                    [person.email],     # Recipient list
                )

                print 'Mail sent to %s %s' % (person.first_name, person.last_name)
