from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.shortcuts import reverse
from django.utils.text import slugify
import uuid

class Location(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True, null=True)

    class Meta:
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Location, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("location-detail", kwargs={"slug": self.slug})

    def __str__(self):
        return self.name.upper()


class Department(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True, null=True)

    class Meta:
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Department, self).save(*args, **kwargs)

    def __str__(self):
        return self.name.upper()


class User(AbstractUser):
    ROLE_CHOICES = (
        ("clerk", "Clerk"),
        ("technician", "Technician"),
        ("manager", "Manager"),
        ("user", "User"),
    )
    uid = models.UUIDField(default=uuid.uuid4, editable=False)
    role = models.CharField(max_length=100, choices=ROLE_CHOICES, default="user")
    job_title = models.CharField(max_length=100, null=True, blank=True)
    department = models.ForeignKey(
        Department, on_delete=models.SET_NULL, null=True, blank=True
    )
    location = models.ForeignKey(
        Location, on_delete=models.SET_NULL, null=True, blank=True
    )
    phone = models.CharField(max_length=7, null=True, blank=True)
    slug = models.SlugField(unique=True, blank=True, null=True)

    class Meta:
        ordering = ["username"]
        app_label = "users"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.uid)
        self.email = self.email.lower()
        self.username = self.username.lower()
        super(User, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("get-user-detail", kwargs={"slug": self.slug})

    def __str__(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return f"{self.email}"