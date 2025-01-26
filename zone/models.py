from django.db import models
from django.contrib.gis.geos import Point
from django.contrib.gis.db import models

class Zone(models.Model):
    name = models.CharField(verbose_name="نام زون",max_length=100, unique=True)
    description = models.TextField(verbose_name="توضیح",null=True, blank=True)
    polygon = models.PolygonField(verbose_name="پلیگان")

    def __str__(self):
        return self.name

    def contains_point(self, latitude, longitude):
        """
        بررسی می‌کند که آیا یک نقطه در محدوده چندضلعی این زون قرار دارد یا نه.
        :param latitude: عرض جغرافیایی نقطه
        :param longitude: طول جغرافیایی نقطه
        :return: True اگر نقطه در زون باشد، در غیر این صورت False
        """
        point = Point(longitude, latitude)  # توجه: ابتدا طول، سپس عرض
        return self.polygon.contains(point)