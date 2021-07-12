from django.db import models

class Contact(models.Model):
    name = models.CharField(max_length=50)
    department = models.CharField(max_length=50)
    adress = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    work_time = models.CharField(max_length=50)
    lat = models.IntegerField()
    lng = models.IntegerField()
    is_active = models.BooleanField() 
    
    class Meta:
        verbose_name = "Contact"
        verbose_name_plural = "Contacts"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Contact_detail", kwargs={"pk": self.pk})


class Feedback(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    phone = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    description = models.TextField()

    class Meta:
        verbose_name = "Feedback"
        verbose_name_plural = "Feedbacks"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Feedback_detail", kwargs={"pk": self.pk})
