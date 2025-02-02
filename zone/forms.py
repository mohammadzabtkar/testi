from django import forms
from .models import Zone
import ast

class ZoneForm(forms.ModelForm):
    class Meta:
        model = Zone
        fields = ['name', 'description', 'polygon']

    polygon = forms.CharField(widget=forms.Textarea, required=True, help_text="مختصات باید به صورت یک لیست از نقاط وارد شود.")

    def clean_polygon(self):
        polygon_str = self.cleaned_data.get('polygon')
        try:
            # تبدیل رشته به لیست
            polygon_coords = ast.literal_eval(polygon_str.strip())  # با .strip() فضاهای اضافی رو حذف می‌کنیم
            if not isinstance(polygon_coords, list):
                raise forms.ValidationError("مختصات باید به صورت لیست وارد شوند.")
            for coord in polygon_coords:
                if not isinstance(coord, list) or len(coord) != 2:
                    raise forms.ValidationError("هر نقطه باید شامل دو مقدار (طول و عرض جغرافیایی) باشد.")
        except Exception:
            raise forms.ValidationError("مختصات وارد شده صحیح نیست.")
        return polygon_coords
