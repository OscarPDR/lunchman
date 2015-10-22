
from django.contrib import admin

from .models import *


###     FirstCourseInline
####################################################################################################

class FirstCourseInline(admin.TabularInline):
    model = FirstCourse
    extra = 2


###     SecondCourseInline
####################################################################################################

class SecondCourseInline(admin.TabularInline):
    model = SecondCourse
    extra = 2


###     DessertInline
####################################################################################################

class DessertInline(admin.TabularInline):
    model = Dessert
    extra = 2


###     MenuAdmin
####################################################################################################

class MenuAdmin(admin.ModelAdmin):
    model = Menu

    inlines = [
        FirstCourseInline,
        SecondCourseInline,
        DessertInline,
    ]


###     MealTicketAdmin
####################################################################################################

class MealTicketAdmin(admin.ModelAdmin):
    model = MealTicket

    list_display = (
        'owner',
        'remaining_meals',
        'purchased',
    )


###     AttendedMealAdmin
####################################################################################################

class AttendedMealAdmin(admin.ModelAdmin):
    model = AttendedMeal

    list_display = (
        'person',
        'date',
    )


###     UserSettingsAdmin
####################################################################################################

class UserSettingsAdmin(admin.ModelAdmin):
    model = UserSettings

    list_display = (
        'user',
        'default_behaviour',
    )


###     Register classes
####################################################################################################

admin.site.register(MealTicket, MealTicketAdmin)
admin.site.register(AttendedMeal, AttendedMealAdmin)
admin.site.register(Menu, MenuAdmin)
admin.site.register(UserSettings, UserSettingsAdmin)
