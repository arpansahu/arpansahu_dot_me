from django.contrib import admin
from .models import Resume


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('file', 'is_active', 'uploaded_at')
    list_filter = ('is_active',)
    actions = ['make_active']

    @admin.action(description='Set selected resume as active')
    def make_active(self, request, queryset):
        if queryset.count() != 1:
            self.message_user(request, 'Please select exactly one resume to activate.', level='error')
            return
        Resume.objects.filter(is_active=True).update(is_active=False)
        queryset.update(is_active=True)
        self.message_user(request, 'Resume activated successfully.')