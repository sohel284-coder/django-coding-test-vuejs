from itertools import count, product
from django.shortcuts import render, redirect
from django.views import generic
from django.db.models import OuterRef, Subquery, Max
from django.shortcuts import get_object_or_404

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from product.forms import ProductForm

from product.models import Product, ProductVariantPrice, Variant, ProductVariant



class CreateProductView(generic.TemplateView):
    template_name = 'products/create.html'

    def get_context_data(self, **kwargs):
        context = super(CreateProductView, self).get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True).values('id', 'title')
        context['product'] = True
        context['variants'] = list(variants.all())
        return context




def edit_product(request, sku):

    product_to_edit = get_object_or_404(Product, sku=sku)
    form = ProductForm(instance=product_to_edit)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product_to_edit)
        if form.is_valid():
            form.save()
            return redirect('product:list.product')
        else:
            form = ProductForm(instance=product_to_edit)

    return render(request, "products/edit.html", {'form': form, 'product': product_to_edit})


def product_list(request, ):

    title = request.GET.get('title')
    product_list = []
    count = Product.objects.all().count()
    min = request.GET.get('price_from')
    max = request.GET.get('price_to')
    date = request.GET.get('date')
    page = request.GET.get('page', 1)

    prod_variants_style = ProductVariant.objects.filter(variant__title="Style").values('variant_title', )
    prod_variants_size = ProductVariant.objects.filter(variant__title="Size").values('variant_title', )
    prod_variants_color = ProductVariant.objects.filter(variant__title="Color").values('variant_title', )

    
     


    if title or (min and max) or date:
        try:
            product_filters_by_title = Product.objects.filter(title__icontains=title)
            products_filter = product_filters_by_title
        except:
            pass

        try:
            product_filters_by_date = Product.objects.filter(created_at__date=date)
            products_filter =  product_filters_by_date

        except:
            pass    
        

        try:
            price_range_ids = ProductVariantPrice.objects.filter(price__range=(min, max)).order_by('price').values('id')
            product_filters_by_price = Product.objects.filter(pk__in=price_range_ids)
            products_filter = product_filters_by_price

        except:
            product_filters_by_price = []     
        
        for p in products_filter:
            dict = {}
            product_variant_price = ProductVariantPrice.objects.filter(product=p.id)
            dict['product'] = p
            dict['product_variant_price_list'] = product_variant_price
            product_list.append(dict)
        
        paginator = Paginator(product_list, 2)
        print(paginator.num_pages)
        try:
            product_list = paginator.page(page)
        except PageNotAnInteger:
            product_list = paginator.page(1)
        except EmptyPage:
            product_list = paginator.page(paginator.num_pages)
        print(paginator)

        return render(request, 'products/list.html', {
                'product_list':product_list,
                'count':count,
        })    
        

    else:
        products = Product.objects.all().order_by('-created_at')
        for p in products:
            dict = {}
            product_variant_price = ProductVariantPrice.objects.filter(product=p.id)
            dict['product'] = p
            dict['product_variant_price_list'] = product_variant_price
            product_list.append(dict)

        paginator = Paginator(product_list, 2)
        print(paginator.num_pages)
        try:
            product_list = paginator.page(page)
        except PageNotAnInteger:
            product_list = paginator.page(1)
        except EmptyPage:
            product_list = paginator.page(paginator.num_pages)
        print(paginator)
        return render(request, 'products/list.html', {
                'product_list':product_list,
                'count':count,
                'prod_variants_style':prod_variants_style,
                'prod_variants_color':prod_variants_color,
                'prod_variants_size':prod_variants_size,

                
        })    
    
