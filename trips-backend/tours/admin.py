from django.contrib import admin
from .models import Tour, TourInstance


class TourInstanceInline(admin.StackedInline):
    model = TourInstance
    extra = 0


class TourAdmin(admin.ModelAdmin):
    inlines = [TourInstanceInline]


admin.site.register(Tour, TourAdmin)
