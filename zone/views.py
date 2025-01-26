from django.http import  HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .models import Zone

# Create your views here.
def zone_list(request):
    queryset = Zone.objects.all()
    context = {"queryset": queryset}
    return render(request, "zone/zone_list.html", context)


class zone_add(CreateView):
    model = Zone
    # permission_required = 'irandepo.add_irandepo'
    fields = ['name', 'description', 'polygon', ]
    template_name = 'zone/zone_add.html'
    success_url = reverse_lazy('zone:zone_list')