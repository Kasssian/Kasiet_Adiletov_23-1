from datetime import datetime
from product.models import Product, Category, Review
from django.shortcuts import HttpResponse, render, redirect
from product.forms import ProductCreateForm, ReviewCreateForm

PAGINATION_LIMIT = 4


def hello(request):
    return HttpResponse(f'Hello {request.user}! Its my project')


def good_bay(request):
    return HttpResponse(f'Good bay {request.user}!')


def check_user(request):
    return None if request.user.is_anonymous else request.user


def now_date(request):
    return HttpResponse(datetime.now().date())


def rend(request):
    if request.method == 'GET':
        return render(request, 'layouts/index.html', context={
            "user": check_user(request)
        })


def products_view(request):
    if request.method == 'GET':
        category_id = request.GET.get('category_id')
        search = request.GET.get('search')
        page = int(request.GET.get('page', 1))

        if category_id:
            products = Product.objects.filter(category_id=category_id)
        else:
            products = Product.objects.all()

        max_page = products.__len__() // PAGINATION_LIMIT

        if round(max_page) < max_page:
            max_page = round(max_page) + 1

        max_page = int(max_page)

        products = products[PAGINATION_LIMIT * (page-1):PAGINATION_LIMIT * page]

        if search:
            products = products.filter(title__icontains=search)


        return render(request, 'products/product.html', context={
            'products': products,
            'user': None if request.user.is_anonymous else request.user,
            'max_page': range(1, max_page+1)
        })


def products_detail_view(request, id):
    if request.method == "GET":
        product = Product.objects.get(id=id)
        return render(request, 'products/detail.html', context={
            'product': product,
            'reviews': product.reviews.all(),
            'categories': product.category,
            'review_form': ReviewCreateForm,
            'user': check_user(request),
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
            'form': ProductCreateForm()
        })

    if request.method == 'POST':
        form = ProductCreateForm(data=request.POST)

        if form.is_valid():
            Product.objects.create(
                image=form.cleaned_data.get('image'),
                author=request.user,
                title=form.cleaned_data.get('title'),
                price=form.cleaned_data.get('price'),
                quantity=form.cleaned_data.get('quantity'),
                creat_date=form.cleaned_data.get('creat_date'),
                description=form.cleaned_data.get('description'),
            )
            Category.objects.get(
                category=request.POST.get('category'),
            )
            return redirect('/products/')
        else:
            return render(request, 'products/create_product.html', context={
                'form': form
            })
