from django.views.generic import ListView, DetailView
from .models import Product
from django.http import Http404
from cart.models import Cart
from renting.forms import RentingOrderForm


class ProductList(ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'product_list'

    def get_context_data(self, *args, **kwargs):
        context = super(ProductList, self).get_context_data(*args, **kwargs)
        context['cart'] = Cart.objects.new_or_get(self.request)[0]
        return context


class ProductDetail(DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product_detail'

    def get_context_data(self, **kwargs):
        context = super(ProductDetail, self).get_context_data(**kwargs)
        context['renting_form'] = RentingOrderForm()
        context['cart'] = Cart.objects.new_or_get(self.request)[0]
        return context

    def get_object(self, *args, **kwargs):
        slug = self.kwargs.get('slug')
        try:
            instance = Product.objects.get(slug=slug, active=True)
        except Product.DoesNotExist:
            raise Http404("Not found..")
        except Product.MultipleObjectsReturned:
            qs = Product.objects.filter(slug=slug, active=True)
            instance = qs.first()
        except:
            raise Http404("Something Went Wrong!")
        return instance