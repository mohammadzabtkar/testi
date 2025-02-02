from django.contrib.gis.geos import Polygon
from django.shortcuts import render
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import ZoneForm
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Zone
from django.contrib.gis.geos import Point


def zone_list(request):
    queryset = Zone.objects.all()
    context = {"queryset": queryset}
    return render(request, "zone/zone_list.html", context)


class ZoneAddView(CreateView):
    model = Zone
    form_class = ZoneForm
    template_name = 'zone/zone_add.html'
    success_url = reverse_lazy('zone:zone_list')

    def form_valid(self, form):
        polygon_coords = form.cleaned_data['polygon']
        try:
            # تبدیل مختصات به شیء Polygon
            polygon = Polygon(polygon_coords)
            form.instance.polygon = polygon  # اختصاص به فیلد مدل
        except Exception as e:
            form.add_error('polygon', 'مختصات وارد شده صحیح نیست')
            return super().form_invalid(form)
        return super().form_valid(form)

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.gis.geos import Point
from .models import Zone

@api_view(['GET'])
def check_point_in_zone(request):
    longitude = request.GET.get('longitude', '').strip()
    latitude = request.GET.get('latitude', '').strip()

    if not longitude or not latitude:
        return Response({"error": "طول و عرض جغرافیایی الزامی است."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        longitude = float(longitude)
        latitude = float(latitude)
    except ValueError:
        return Response({"error": "مختصات وارد شده نامعتبر است."}, status=status.HTTP_400_BAD_REQUEST)

    # ایجاد یک نقطه جغرافیایی
    user_point = Point(longitude, latitude)

    # بررسی وجود زونی که این نقطه را شامل می‌شود
    zone = Zone.objects.filter(polygon__contains=user_point).first()

    if zone:
        return Response({
            "نام زون": zone.name,
            "توضیحات": zone.description or "بدون توضیح",
        }, status=status.HTTP_200_OK)
    else:
        return Response({"error": "هیچ زونی شامل این نقطه نیست."}, status=status.HTTP_404_NOT_FOUND)
