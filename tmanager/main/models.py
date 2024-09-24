from django.contrib.auth.models import User
from django.db import models

class Saller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField('Имя', max_length=100)
    last_name = models.CharField('Фамилия', max_length=100)
    date_registered = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class Material(models.Model):
    name_n = models.CharField('Название материала', max_length=100)
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    saller = models.ForeignKey(Saller, related_name='materials', on_delete=models.CASCADE)

    def __str__(self):
        return self.name_n