from django.urls import path


from product.api.views import ProductVariationPriceAPIView, ProductEditAPIView

urlpatterns = [
    path('create-product/', ProductVariationPriceAPIView.as_view(), name=''),
    path('product/<slug:sku>/', ProductEditAPIView.as_view(), name=''),

    
]
