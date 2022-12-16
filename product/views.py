from datetime import datetime
from product.models import Product
from django.shortcuts import HttpResponse, render


def hello(request):
    return HttpResponse(f'Hello {request.user}! Its my project')


def good_bay(request):
    return HttpResponse(f'Good bay {request.user}!')


def now_date(request):
    return HttpResponse(datetime.now().date())


def rend(request):
    return render(request, 'layouts/index.html')


def products_view(request):
    if request.method == 'GET':
        products = Product.objects.all()
        return render(request, 'products/product.html', context={
            'products': products
        })
