from django.db import models # type: ignore
#from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.translation import gettext as _ # type: ignore
from django.contrib.auth.models import User # type: ignore


from django.contrib.auth.models import AbstractUser # type: ignore
from django.db import models # type: ignore

class Categoria(models.Model):
    nombre = models.CharField(max_length=200)
    def __str__(self):
        return self.nombre

class Tarea(models.Model):
    OPCIONES_ESTADO = (
        ('PENDIENTE', 'Pendiente'),
        ('EN_PROGRESO', 'En Progreso'),
        ('COMPLETADA', 'Completada'),
    )
    OPCIONES_PRIORIDAD = (
        ('BAJA', 'Baja'),
        ('MEDIA', 'Media'),
        ('ALTA', 'Alta'),
    )
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    fecha_vencimiento = models.DateTimeField()
    estado = models.CharField(max_length=12, choices=OPCIONES_ESTADO, default='PENDIENTE')
    prioridad = models.CharField(max_length=6, choices=OPCIONES_PRIORIDAD, default='MEDIA')
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    asignada_a = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tareas_asignadas')
    es_publica = models.BooleanField(default=False)
	
    def comentarios_publicos(self):
        return self.comentario_set.filter(visibilidad='PUBLICO').count()

    def __str__(self):
	    
        visibilidad = "Pública" if self.es_publica else "Privada"
        return '{} ({}) - {} - {}'.format(self.nombre, self.asignada_a, visibilidad, self.estado)	
    

class Comentario(models.Model):
    OPCIONES_VISIBILIDAD = (
        ('PUBLICO', 'Publico'),
        ('PRIVADO', 'Privado'),
    )
    texto = models.TextField()
    creado_por = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comentario_usuario')
    tarea = models.ForeignKey(Tarea, on_delete=models.CASCADE)
    visibilidad = models.CharField(max_length=7, choices=OPCIONES_VISIBILIDAD, default='PUBLICO')
    
    def __str__(self):
        visibilidad = "Público" if self.visibilidad=="PUBLICO" else "Privado"
        return '{} ({}) - {}'.format(self.texto, self.creado_por.username, visibilidad)

