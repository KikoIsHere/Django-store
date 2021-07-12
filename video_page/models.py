from django.db import models
from ckeditor.fields import RichTextField


class Video(models.Model):
    title = models.CharField(max_length=50)
    description = RichTextField()
    album = models.ImageField(upload_to='images', blank=True)
    uploads = models.FileField(upload_to='uploads', blank=True)
    link = models.URLField(max_length=256)
    slug = models.SlugField()
    meta_description = models.CharField(max_length=256)
    meta_keyword = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Video"
        verbose_name_plural = "Videos"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("Video_detail", kwargs={"slug": self.slug})

