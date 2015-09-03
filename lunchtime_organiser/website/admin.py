
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


###     Register classes
####################################################################################################

admin.site.register(MealTicket)
admin.site.register(AttendedMeal)
admin.site.register(Menu, MenuAdmin)
