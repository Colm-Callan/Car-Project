from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Product, Comment
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.views.generic.edit import CreateView, DeleteView
from django.views.generic import DetailView, ListView
from django.urls import reverse_lazy
from .forms import CommentForm


def prod_list(request, category_id=None):
    category = None
    products = Product.objects.filter(available=True)
    if category_id:
        category = get_object_or_404(Category, id=category_id)
        products = Product.objects.filter(category=category, available=True)

    paginator = Paginator(products, 6)
    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1
    try:
        products = paginator.page(page)
    except (EmptyPage,InvalidPage):
        products = paginator.page(paginator.num_pages)

        
    return render(request, 'shop/category.html',{'category':category, 'prods':products})


def product_detail(request, category_id, product_id):
    product = get_object_or_404(Product, category_id=category_id, id=product_id)
    return render(request, 'shop/product.html', {'product': product})


class CarCreateView(CreateView):
    model = Product
    template_name = 'temp_car/car_create.html'
    fields = ['name', 'description', 'category', 'price', 'image', 'stock', 'available']



class CarDetailView(DetailView):
    model = Product
    template_name = 'temp_car/car_detail.html'

class CarListView(ListView):
    model = Product
    context_object_name = "car_list"
    template_name = 'temp_car/car_list.html'

class CarDeleteView(DeleteView):
    model = Product
    template_name = 'temp_car/car_delete.html'
    success_url = reverse_lazy('car_list')
    
def add_comment(request, pk):
    car = get_object_or_404(Product, pk=pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        author = request.user
        comment = form.cleaned_data['comment']
        commentObject = Comment(car = car, comment=comment, author = author)
        commentObject.save()

        return redirect('car_detail', car.pk)

    form = CommentForm()
    context = {
        "car":car,
        "form":form
    }
    return render(request, 'temp_comments/comment_create.html', context)
