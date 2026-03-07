from django.db import models

class Menu(models.Model):
    name = models.CharField(max_length=200)
    price = models.IntegerField()
    menu_item_description = models.TextField(max_length=1000, default='')

    def __str__(self):
       return self.name