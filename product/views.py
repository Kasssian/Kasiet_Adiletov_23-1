from datetime import datetime
from product.models import Product, Category, Review
from django.shortcuts import HttpResponse, render, redirect
from product.forms import ProductCreateForm, ReviewCreateForm


def hello(request):
    return HttpResponse(f'Hello {request.user}! Its my project')


def good_bay(request):
    return HttpResponse(f'Good bay {request.user}!')


def check_user(request):
    return None if request.user.is_anonymous else request.user


def now_date(request):
    return HttpResponse(datetime.now().date())


def rend(request):
    if request.method == "GET":
        return render(request, 'layouts/index.html', context={
            "user": check_user(request)
        })


def products_view(request):
    if request.method == 'GET':
        category_id = request.GET.get('category_id')
        if category_id:
            products = Product.objects.filter(category_id=category_id)
        else:
            products = Product.objects.all()
        return render(request, 'products/product.html', context={
            'products': products,
            'user': None if request.user.is_anonymous else request.user
        })


def products_detail_view(request, id):
    if request.method == "GET":
        product = Product.objects.get(id=id)
        return render(request, 'products/detail.html', context={
            'product': product,
            'reviews': product.reviews.all(),
            'categories': product.category,
            'review_form': ReviewCreateForm,
        })
    if request.method == "POST":
        product = Product.objects.get(id=id)
        form = ReviewCreateForm(data=request.POST)

        if form.is_valid():
            Review.objects.create(
                product_id=id,
                author=form.cleaned_data.get('author'),
                text=form.cleaned_data.get('text'),
            )
            return redirect(f'/products/{id}/')
        else:
            return render(request, 'products/detail.html', context={
                'product': product,
                'reviews': product.reviews.all(),
                'categories': product.category,
                'review_form': form,
            })


def categories_list_view(request):
    if request.method == "GET":
        categories = Category.objects.all()
        return render(request, 'categories/index.html', context={
            'categories': categories,
            "user": check_user(request)
        })


def product_create_view(request):
    if request.method == "GET":
        return render(request, 'products/create_product.html', context={
            'form': ProductCreateForm
        })

    if request.method == 'POST':
        form = ProductCreateForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            print('valid')
            Product.objects.create(
                author=request.user,
                title=request.POST.get('title'),
                price=request.POST.get('price'),
                quantity=request.POST.get('quantity'),
                creat_date=request.POST.get('creat_date'),
                description=request.POST.get('description'),
            )
            Category.objects.get(
                category=request.POST.get('category'),
            )
            return redirect('/products/')
        else:
            print('not valid')
            print(form.errors)
            return render(request, 'products/create_product.html', context={
                'form': form
            })
