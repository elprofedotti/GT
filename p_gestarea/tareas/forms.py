from django import forms
from .models import Tarea

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
