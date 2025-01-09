from django.db import models

class Banner(models.Model):
    title = models.CharField(max_length=255, help_text="Title of the banner")
    description = models.TextField(blank=True, null=True, help_text="Optional description")
    image = models.ImageField(upload_to='banners/', help_text="Upload the banner image")
    active = models.BooleanField(default=True, help_text="Check to display this banner")

    def __str__(self):
        return self.title

