from django import forms
from product.models import Category

CATEGORY_CHOICES = ((category.title, category) for category in Category.objects.all())


class ProductCreateForm(forms.Form):
    image = forms.FileField()
    title = forms.CharField(max_length=100)
    price = forms.IntegerField(min_value=0)
    quantity = forms.IntegerField(min_value=0)
    creat_date = forms.DateField()
    description = forms.CharField(widget=forms.Textarea)
    category = forms.ChoiceField(choices=CATEGORY_CHOICES)


class ReviewCreateForm(forms.Form):
    customer = forms.CharField(max_length=50, label='Написать имя: ')
    text = forms.CharField(min_length=0, label='Написать комментарий: ')
