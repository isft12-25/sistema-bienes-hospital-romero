# core/forms.py
from django import forms
from .models import BienPatrimonial


# ========== FORMULARIO DE CARGA MASIVA ==========
class CargaMasivaForm(forms.Form):
    archivo_excel = forms.FileField(
        label='Seleccionar archivo Excel',
        help_text='Formatos soportados: .xlsx, .xls',
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )
    sector = forms.CharField(
        max_length=100,
        required=False,
        label='Sector por defecto (opcional)',
        help_text='Si se deja vacío, se tomará el sector de cada fila del archivo.',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )


# ========== FORMULARIO DE BIENES PATRIMONIALES ==========
class BienPatrimonialForm(forms.ModelForm):
    class Meta:
        model = BienPatrimonial
        fields = [
            # NO incluir clave_unica ni nombre (se generan o no se usan en la vista)
            'descripcion',
            'cantidad',
            'expediente',
            'cuenta_codigo',
            'nomenclatura_bienes',
            'numero_serie',
            'numero_identificacion',
            'origen',
            'estado',
            'servicios',
            'observaciones',
            'valor_adquisicion',
            'fecha_adquisicion',
            'fecha_baja',
        ]
        labels = {
            'descripcion': 'Descripción',
            'cantidad': 'Cantidad',
            'expediente': 'N° de Expediente',
            'cuenta_codigo': 'Cuenta Código',
            'nomenclatura_bienes': 'Nomenclatura de Bienes',
            'numero_serie': 'N° de Serie',
            'numero_identificacion': 'N° de ID',
            'origen': 'Origen',
            'estado': 'Estado',
            'servicios': 'Servicios / Sector',
            'observaciones': 'Observaciones',
            'valor_adquisicion': 'Precio',
            'fecha_adquisicion': 'Fecha de Alta',
            'fecha_baja': 'Fecha de Baja',
        }
        widgets = {
            'descripcion': forms.Textarea(attrs={
                'rows': 2,
                'class': 'form-control',
                'placeholder': 'Ingrese una descripción del bien...'
            }),
            'cantidad': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1
            }),
            'expediente': forms.Select(attrs={'class': 'form-select'}),
            'cuenta_codigo': forms.TextInput(attrs={
                'class': 'form-control',
                'maxlength': 50
            }),
            'nomenclatura_bienes': forms.TextInput(attrs={
                'class': 'form-control',
                'maxlength': 200
            }),
            'numero_serie': forms.TextInput(attrs={
                'class': 'form-control',
                'maxlength': 255
            }),
            'numero_identificacion': forms.TextInput(attrs={
                'class': 'form-control',
                'maxlength': 255
            }),
            'origen': forms.Select(attrs={'class': 'form-select'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'servicios': forms.TextInput(attrs={
                'class': 'form-control',
                'maxlength': 200
            }),
            'observaciones': forms.Textarea(attrs={
                'rows': 2,
                'class': 'form-control',
                'placeholder': 'Agregue observaciones si las hubiera...'
            }),
            'valor_adquisicion': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': 0
            }),
            'fecha_adquisicion': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'fecha_baja': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
        }
