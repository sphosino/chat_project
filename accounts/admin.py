from django.contrib import admin
from .models import CustomUser, PushSubscription
from user_profile.models import Profile

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False

class PushSubscriptionInLine(admin.TabularInline):
    model = PushSubscription
    extra = 0
    readonly_fields = ("endpoint", "created_at")

class CustomUserAdmin(admin.ModelAdmin):
    inlines = (ProfileInline, PushSubscriptionInLine)

admin.site.register(CustomUser, CustomUserAdmin)