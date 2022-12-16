from django.db import models


# Create your models here.

class Product(models.Model):
    image = models.ImageField(blank=True, verbose_name="Изображение")
    title = models.CharField(max_length=100)
    price = models.FloatField()
    quantity = models.PositiveIntegerField()
    creat_date = models.DateField()
    description = models.TextField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"