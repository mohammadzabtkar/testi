from django import forms
from django.contrib import admin
from django.contrib.gis.geos import GEOSGeometry
from .models import Zone

class ZoneAdminForm(forms.ModelForm):
    class Meta:
        model = Zone
        fields = '__all__'

    # تنظیم ویجت Textarea برای فیلد polygon
    polygon = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3, 'cols': 50}),
        help_text="مختصات چندضلعی را با فرمت WKT وارد کنید. مثال: POLYGON((x1 y1, x2 y2, x3 y3, x1 y1))"
    )

    def clean_polygon(self):
        polygon_data = self.cleaned_data.get('polygon')
        try:
            # بررسی اینکه داده ورودی یک چندضلعی معتبر باشد
            geom = GEOSGeometry(polygon_data)
            if geom.geom_type != 'Polygon':
                raise forms.ValidationError("مختصات وارد شده باید یک چندضلعی معتبر (Polygon) باشد.")
            return geom
        except Exception as e:
            raise forms.ValidationError(f"خطا در مختصات وارد شده: {e}")

@admin.register(Zone)
class ZoneAdmin(admin.ModelAdmin):
    form = ZoneAdminForm
    list_display = ('name', 'description')
