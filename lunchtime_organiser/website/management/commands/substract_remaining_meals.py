
from django.core.management.base import BaseCommand
from website.models import AttendedMeal, MealTicket

import datetime


class Command(BaseCommand):

    help = u"Substract meal count for today's attendees"

    def handle(self, *args, **options):

        today = datetime.date.today()

        attendee_ids = AttendedMeal.objects.filter(date=today).values_list('person__id', flat=True)

        for person_id in attendee_ids:
            lesser_meal_ticket = MealTicket.objects.filter(owner=person_id, remaining_meals__gt=0).order_by('remaining_meals').first()

            lesser_meal_ticket.remaining_meals = lesser_meal_ticket.remaining_meals - 1
            lesser_meal_ticket.save()
