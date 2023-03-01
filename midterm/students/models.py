from django.db import models


class Student(models.Model):
    name = models.CharField(max_length=255, verbose_name='Имя')
    surname = models.CharField(max_length=255, verbose_name='Фамилия')
    year_of_study = models.IntegerField(verbose_name='Год обучения')
