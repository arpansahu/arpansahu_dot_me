from django.db import models


class Resume(models.Model):
    file = models.FileField(upload_to='pdfs/')
    is_active = models.BooleanField(default=False, help_text='Only one resume can be active at a time')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        status = '(Active)' if self.is_active else '(Inactive)'
        return f'{self.file.name} {status}'

    def save(self, *args, **kwargs):
        # Ensure only one resume is active at a time
        if self.is_active:
            Resume.objects.filter(is_active=True).exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)