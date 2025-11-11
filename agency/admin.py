from django.contrib import admin

from .models import Cat, Mission, Target


@admin.register(Cat)
class CatAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "breed", "years_of_experience", "salary")
    search_fields = ("name", "breed")


class TargetInline(admin.TabularInline):
    model = Target
    extra = 0


@admin.register(Mission)
class MissionAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "cat", "is_completed", "created_at")
    inlines = [TargetInline]


@admin.register(Target)
class TargetAdmin(admin.ModelAdmin):
    list_display = ("id", "mission", "name", "country", "is_completed")
    list_filter = ("is_completed", "country")
