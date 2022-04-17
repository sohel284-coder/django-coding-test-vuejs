from inspect import stack
from itertools import product
from wsgiref import validate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import get_object_or_404

from product.api.serializers import ProductVariationPriceSerializer, ProductSerializer

from product.models import Product, ProductVariant, Variant, ProductVariantPrice





class ProductVariationPriceAPIView(APIView):

    def post(self, request, format=None):
        serializer = ProductVariationPriceSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            validated_data = serializer.validated_data
            print(validated_data)
            title = validated_data['title']
            sku = validated_data['sku']
            description = validated_data['description']
            product = Product.objects.create(title=title, sku=sku, description=description)
            
            product_variants = validated_data['product_variant']
            for pv in product_variants:
                # Product variant creat for Size   
                if pv['option'] == 1:
                    variant = 'Size'
                    variant_instance = Variant.objects.get(title=variant)
                    tags = pv['tags']
                    for tag in tags:
                        product_variant = ProductVariant.objects.create(variant_title=tag, variant=variant_instance, product=product)
                    print(product_variant)

                # Product variant create for Color

                if pv['option'] == 2:
                    variant = 'Color'
                    variant_instance = Variant.objects.get(title=variant)
                    tags = pv['tags']
                    for tag in tags:
                        product_variant = ProductVariant.objects.create(variant_title=tag, variant=variant_instance, product=product)
                    print(product_variant)

                # Product variant create for Color
                if pv['option'] == 3:
                    variant = 'Style'
                    variant_instance = Variant.objects.get(title=variant)
                    tags = pv['tags']
                    for tag in tags:
                        product_variant = ProductVariant.objects.create(variant_title=tag, variant=variant_instance, product=product)
                    print(product_variant)           
            
            #Product Varient price Object Create here
            product_variant_prices = validated_data['product_variant_prices']
            for pvp in product_variant_prices:
                titles = pvp['title'].split('/',)[:-1]
                try:
                    product_variant_one_instance = ProductVariant.objects.get(variant_title=titles[0], product=product)
                except:
                    product_variant_one_instance = None
                try:
                    product_variant_two_instance = ProductVariant.objects.get(variant_title=titles[1], product=product)
                except:
                    product_variant_two_instance = None
                try:
                    product_variant_three_instance = ProductVariant.objects.get(variant_title=titles[2], product=product)
                except:
                    product_variant_three_instance = None  
                
                product_variant_price = ProductVariantPrice.objects.create(
                    product_variant_one=product_variant_one_instance,
                    product_variant_two=product_variant_two_instance,
                    product_variant_three=product_variant_three_instance,
                    price=pvp['price'],
                    stock=pvp['stock'],
                    product=product
                )
                print(product_variant_price)
                
            return Response('Successfully saved', status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductEditAPIView(APIView):
    
    def get_product_instance(self, slug):
        product = get_object_or_404(Product, sku=slug)
        return product

    def get(self, request, slug, format=None):
        product = self.get_product_instance(slug)
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK) 

  

    def put(self, request, slug, format=None):
        product = self.get_product_instance(slug)
        serializer = ProductSerializer(product, data=request.data, )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK) 

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            