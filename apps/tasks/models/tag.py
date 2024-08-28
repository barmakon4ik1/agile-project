from django.db import models
from django.core.validators import MinLengthValidator


class Tag(models.Model):
    name = models.CharField(max_length=20, validators=[MinLengthValidator(4)])

    def __str__(self):
        return self.name
