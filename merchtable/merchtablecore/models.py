from django.db import models
from django.core.validators import MinValueValidator
import uuid

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile

# Store default photo
filename = settings.BASE_DIR / "merchtable/static/media/default_photo.jpg"
file = open(filename, 'rb')
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
        return self.name + " (" + self.payment + ")"


class Item(models.Model):

    class Meta:
        ordering = ["name"]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0.01)])
    photo = models.ImageField(blank=True, null=True)
    seller = models.ForeignKey("Seller", related_name="items", on_delete=models.CASCADE)

    def __str__(self):
        return str(self.seller.name) + " - " + self.name + ": $" + str(self.price)
