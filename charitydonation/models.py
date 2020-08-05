from django.db import models
from django.conf import settings

INSTITUTION_TYPES = (
    ('Fundacja', 'Fundacja'),
    ('Organizacja pozarządowa', 'Organizacja pozarządowa'),
    ('Zbiórka lokalna', 'Zbiórka lokalna')
)

class Category(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class Institution(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField()
    type = models.CharField(max_length=32, choices=INSTITUTION_TYPES, default='Fundacja')
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.name


class Donation(models.Model):
    quantity = models.IntegerField()
    categories = models.ManyToManyField(Category)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    address = models.CharField(max_length=64)
    phone_number = models.CharField(max_length=16)
    city = models.CharField(max_length=32)
    zip_code = models.CharField(max_length=8)
    pick_up_date = models.DateField()
    pick_up_time = models.TimeField()
    pick_up_comment = models.CharField(max_length=128)
    is_taken = models.BooleanField(default=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, default=None)

    def __str__(self):
        return 'donation {} - {}'.format(self.quantity, self.address)
