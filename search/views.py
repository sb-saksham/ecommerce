from django.shortcuts import render
from django.db.models import Q
from django.views.generic import ListView
from products.models import Product


class SearchQuery(ListView):
    template_name = "search/search_query.html"
    context_object_name = "products"

    def get_context_data(self, *args, **kwargs):
        context = super(SearchQuery, self).get_context_data(*args, **kwargs)
        query = self.request.GET.get('q')
        context['query'] = query
        # SearchQuery.objects.create(query=query)
        return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        query = request.GET.get('q', None)
        if query is not None:
            return Product.objects.search(query)
        else:
            return Product.objects.all()
