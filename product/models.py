from django.db import models


# Create your models here.

class Product(models.Model):
    image = models.ImageField(blank=True, verbose_name="Изображение")
    title = models.CharField(max_length=100, verbose_name="Название")
    price = models.FloatField(verbose_name="Цена")
    quantity = models.PositiveIntegerField(verbose_name="Количество")
    creat_date = models.DateField(verbose_name="Дата создания")
    description = models.TextField(verbose_name="Описание")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, related_name="reviews")
    customer = models.CharField(max_length=50, verbose_name="Покупатель", default="Аноним")
    text = models.TextField(verbose_name="Отзыв")
    creat_date = models.DateField(auto_now=True)

    def __str__(self):
        return self.customer

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
