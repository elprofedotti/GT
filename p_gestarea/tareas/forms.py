from django import forms
from .models import Tarea, Categoria

#class TareaForm(forms.ModelForm):
    # class Meta:
        # model = Tarea
        # fields = ['nombre', 'descripcion', 'fecha_vencimiento', 'estado', 'prioridad', 'categoria', 'asignada_a', 'es_publica']

class CambioTareaForm(forms.Form):
    OPCIONES_ESTADO = (
        ('PENDIENTE', 'Pendiente'),
        ('EN_PROGRESO', 'En Progreso'),
        ('COMPLETADA', 'Completada'),
    )
    
    OPCIONES_VISIBILIDAD = (
        ('PUBLICO', 'Publico'),
        ('PRIVADO', 'Privado'),
    )
    
    estado = forms.ChoiceField(choices=OPCIONES_ESTADO)
    visibilidad = forms.ChoiceField(choices=OPCIONES_VISIBILIDAD)
    comentario = forms.CharField(widget=forms.Textarea, required=False)
    
class TareaForm(forms.ModelForm):
    class Meta:
        model = Tarea
        fields = ['nombre', 'descripcion', 'fecha_vencimiento', 'estado', 'prioridad', 'categoria', 'es_publica']
        widgets = {
            'fecha_vencimiento': forms.DateInput(attrs={'type': 'date'}),
        }


class TareaFormSQL(forms.ModelForm):
    nombre = forms.CharField(max_length=200)
    descripcion = forms.CharField(widget=forms.Textarea)
    fecha_vencimiento = forms.DateTimeField(widget=forms.DateInput(attrs={'type': 'date'}))
    estado = forms.ChoiceField(choices=[('PENDIENTE', 'Pendiente'), ('EN_PROGRESO', 'En Progreso'), ('COMPLETADA', 'Completada')])
    prioridad = forms.ChoiceField(choices=[('BAJA', 'Baja'), ('MEDIA', 'Media'), ('ALTA', 'Alta')])
    categoria = forms.ModelChoiceField(queryset=Categoria.objects.all())
    es_publica = forms.BooleanField(required=False)

