from django.urls import path
from django.views.generic import TemplateView

from product.views.product import CreateProductView, product_list, edit_product
from product.views.variant import VariantView, VariantCreateView, VariantEditView



app_name = "product"

urlpatterns = [
    # Variants URLs
    
    path('variants/', VariantView.as_view(), name='variants'),
    path('variant/create', VariantCreateView.as_view(), name='create.variant'),
    path('variant/<int:id>/edit', VariantEditView.as_view(), name='update.variant'),

    # Products URLs
    path('create/', CreateProductView.as_view(), name='create.product'),
    path('edit/<slug:sku>/', edit_product, name='edit.product'),

    path('list/', product_list, name="list.product"),
   
]
