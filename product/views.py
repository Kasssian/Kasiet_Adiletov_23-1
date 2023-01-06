from datetime import datetime
from product.models import Product, Category, Review
from django.shortcuts import HttpResponse, render, redirect
from product.forms import ProductCreateForm, ReviewCreateForm
from django.views.generic import ListView, DetailView, FormView, CreateView

PAGINATION_LIMIT = 4


def check_user(request):
    return None if request.user.is_anonymous else request.user


def rend(request):
    if request.method == 'GET':
        return render(request, 'layouts/index.html', context={
            "user": check_user(request)
        })


class ProductsCBV(ListView):
    queryset = Product.objects.all()
    template_name = 'products/product.html'

    def get(self, request, **kwargs):
        category_id = request.GET.get('category_id')
        search = request.GET.get('search')
        page = int(request.GET.get('page', 1))

        if category_id:
            products = self.queryset.filter(category_id=category_id)
        else:
            products = self.queryset

        if search:
            products = products.filter(title__icontains=search)

        max_page = products.__len__() // PAGINATION_LIMIT

        if round(max_page) < max_page:
            max_page = round(max_page) + 1

        max_page = int(max_page)

        products = products[PAGINATION_LIMIT * (page - 1):PAGINATION_LIMIT * page]

        return render(request, self.template_name, context={
            'products': products,
            'user': None if request.user.is_anonymous else request.user,
            'max_page': range(1, max_page + 1)
        })


class ProductsDetailCBV(DetailView, CreateView):
    queryset = Product.objects.all()
    context_object_name = "product"
    template_name = "products/detail.html"
    form_class = ReviewCreateForm

    def get(self, request, pk=None):
        product = Product.objects.get(pk=pk)
        return render(request, self.template_name, context={
            "review_form": self.form_class,
            "product": product,
            'reviews': product.reviews.all(),
            "categories": product.category,
            "user": check_user(request)
        })

    def post(self, request, pk=None):
        form = self.form_class(request.POST)
        if form.is_valid():
            Review.objects.create(
                product_id=pk,
                author_id=request.user.id,
                text=form.cleaned_data.get("text")
            )
            return redirect("/products/{}/".format(pk))


class CategoriesCBV(ListView):
    queryset = Category.objects.all()
    template_name = 'categories/index.html'

    def get(self, request):
        return render(request, self.template_name, context={
            'categories': Category.objects.all(),
            'user': check_user(request)
        })


class ProductCreateCBV(FormView):
    template_name = 'products/create_product.html'
    form_class = ProductCreateForm

    # def get_context_data(self, **kwargs):
    #     context = super(ProductCreateCBV, self).get_context_data(**kwargs)
    #     context["form"] = self.form_class
    #     return context
    def get(self, request, *args):
        return render(request, self.template_name, context={
            'form': self.form_class,
            'user': check_user(request),
        })
    #

# def product_create_view(request):
#     if request.method == "GET":
#         return render(request, 'products/create_product.html', context={
#             'form': ProductCreateForm()
#         })
#
#     if request.method == 'POST':
#         form = ProductCreateForm(data=request.POST)
#
#         if form.is_valid():
#             Product.objects.create(
#                 image=form.cleaned_data.get('image'),
#                 author=request.user,
#                 title=form.cleaned_data.get('title'),
#                 price=form.cleaned_data.get('price'),
#                 quantity=form.cleaned_data.get('quantity'),
#                 creat_date=form.cleaned_data.get('creat_date'),
#                 description=form.cleaned_data.get('description'),
#             )
#             Category.objects.get(
#                 category=request.POST.get('category'),
#             )
#             return redirect('/products/')
#         else:
#             return render(request, 'products/create_product.html', context={
#                 'form': form
#             })
