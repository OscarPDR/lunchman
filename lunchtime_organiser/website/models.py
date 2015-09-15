
# coding: utf-8

from django.db import models
from django.contrib.auth.models import User


TIME_CHOICES = (
    ('ordinary', 'Subo a las 13h'),
    ('delayed', 'Subo más tarde, esperad'),
    ('non-attending', 'No subo'),
)


###     MealTicket
####################################################################################################

class MealTicket(models.Model):

    owner = models.ForeignKey(User)

    remaining_meals = models.PositiveSmallIntegerField(
        default=20,
    )

    purchased = models.DateField(
        auto_now_add=True,
    )

    class Meta:
        unique_together = ('owner', 'purchased')

    def __unicode__(self):
        return '%s %s - %s (%d)' % (self.owner.first_name, self.owner.last_name, self.purchased, self.remaining_meals)


###     AttendedMeal
###################################################################################################

class AttendedMeal(models.Model):

    person = models.ForeignKey(User)

    date = models.DateField()

    preferred_time = models.CharField(
        max_length=15,
        default='ordinary',
        choices=TIME_CHOICES,
    )

    class Meta:
        unique_together = ('person', 'date')


###     Menu
###################################################################################################

class Menu(models.Model):

    date = models.DateField(
        unique=True,
    )

    def __unicode__(self):
        return u'%s' % (self.date)

    class Meta:
        ordering = ['-date']


###     FirstCourse
###################################################################################################

class FirstCourse(models.Model):

    menu = models.ForeignKey('Menu')

    meal = models.CharField(
        max_length=75,
    )

    def save(self, *args, **kwargs):

        self.meal = self.meal.replace('c/', 'con ')

        if ' /' in self.meal:
            self.meal = self.meal[:self.meal.rfind(' /')]

        super(FirstCourse, self).save(*args, **kwargs)


###     SecondCourse
###################################################################################################

class SecondCourse(models.Model):

    menu = models.ForeignKey('Menu')

    meal = models.CharField(
        max_length=75,
    )

    def save(self, *args, **kwargs):

        self.meal = self.meal.replace('c/', 'con ')

        if ' /' in self.meal:
            self.meal = self.meal[:self.meal.rfind(' /')]

        super(SecondCourse, self).save(*args, **kwargs)


###     Dessert
###################################################################################################

class Dessert(models.Model):

    menu = models.ForeignKey('Menu')

    meal = models.CharField(
        max_length=75,
    )

    def save(self, *args, **kwargs):

        self.meal = self.meal.replace('c/', 'con ')

        if ' /' in self.meal:
            self.meal = self.meal[:self.meal.rfind(' /')]

        super(Dessert, self).save(*args, **kwargs)
