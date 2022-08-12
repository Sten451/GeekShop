from django.db import models

class Custom_Settings(models.Model):
    count_pagination = models.PositiveSmallIntegerField(default=3, verbose_name='Значение пагинации')