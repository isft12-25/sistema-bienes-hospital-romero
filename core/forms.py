# core/forms.py
from django import forms
from .models import BienPatrimonial

class CargaMasivaForm(forms.Form):
    archivo_excel = forms.FileField(
        label='Seleccionar archivo Excel',
        help_text='Formatos soportados: .xlsx, .xls'
    )
    sector = forms.CharField(
        max_length=100,
        required=False,
        help_text='Sector por defecto (opcional). Si viene vacío, se usa el de cada fila.'
    )
    
class BienPatrimonialForm(forms.ModelForm):
    class Meta:
        model = BienPatrimonial
        fields = [
            'clave_unica', 'nombre', 'descripcion', 'cantidad', 'expediente',
            'cuenta_codigo', 'nomenclatura_bienes', 'fecha_adquisicion',
            'origen', 'estado', 'numero_serie', 'valor_adquisicion',
            'numero_identificacion', 'servicios'
        ]
        widgets = {
            'fecha_adquisicion': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }