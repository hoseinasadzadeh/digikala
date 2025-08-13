from django.shortcuts import render, redirect
from . import models
from django.contrib import messages
from django.db.models import Q

def shopPage(request):
    all_products = models.Product.objects.all()
    return render(request, "shop.html", {"products": all_products})


def product(request, pk):
    product = models.Product.objects.get(id=pk)
    return render(request, "product.html", {"product": product})


def category(request, cat):
    cat = cat.replace("-", " ")
    try:
        cat = models.Category.objects.get(tag=cat)
        products = models.Product.objects.filter(product_category=cat)
        return render(request, "category.html", {"products": products, 'category': category})
    except:
        messages.error(request, 'دسته بندی وجود ندارد')
        return redirect('notfound')


def category_summary(request):
    all_category = models.Category.objects.all()
    return render(request, "category_summary.html", {'all_category': all_category})


def search(request):
    searchName = ''
    searchProducts = []
    has_searched = False
    if request.method == 'POST':
        searchName = request.POST.get('searchName', '').strip()
        has_searched = True
        if searchName:
            searchProducts = models.Product.objects.filter(Q(product_name__icontains = searchName) | Q(product_describtion__icontains = searchName))
            return render(request, 'search.html', {'searchProducts': searchProducts,'searchName': searchName,'has_searched': has_searched})
    
    return render(request, 'search.html', {'has_searched': has_searched})