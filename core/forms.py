# core/forms.py
from django import forms

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
    