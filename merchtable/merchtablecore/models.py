from django.db import models
import uuid

from django.core.files.uploadedfile import SimpleUploadedFile
import os
from django.conf import settings


dir_path = settings.BASE_DIR / "merchtable/static/media"

file = open(os.path.join(dir_path, "default_photo.jpg"), 'rb')
default_pic = SimpleUploadedFile("default_photo.jpg", file.read(), content_type="image")
file.close()


class Seller(models.Model):

    class Meta:
        ordering = ["name"]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100)
    payment = models.CharField(max_length=100)
    photo = models.ImageField(default=default_pic)

    def __str__(self):
        return self.name


class Item(models.Model):

    class Meta:
        ordering = ["name"]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    photo = models.ImageField(default=default_pic)
    seller = models.ForeignKey("Seller", related_name="items", on_delete=models.CASCADE)

    def __str__(self):
        return self.name + ": " + str(self.price)
