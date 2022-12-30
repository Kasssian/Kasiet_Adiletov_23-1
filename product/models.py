from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Category(models.Model):
    image = models.ImageField(null=True, verbose_name="Иконка")
    title = models.CharField(max_length=30, verbose_name="Название категории")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Product(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(blank=True, verbose_name="Изображение")
    title = models.CharField(max_length=100, verbose_name="Название")
    price = models.FloatField(verbose_name="Цена")
    quantity = models.PositiveIntegerField(verbose_name="Количество")
    creat_date = models.DateField(verbose_name="Дата создания")
    description = models.TextField(verbose_name="Описание")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True, related_name="products")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"


class Review(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, related_name="reviews")
    text = models.TextField(verbose_name="Отзыв")
    creat_date = models.DateField(auto_now=True)

    def __str__(self):
        return self.author

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
