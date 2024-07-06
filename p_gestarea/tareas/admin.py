from django.contrib import admin

#Aca se registran los modelos
from .models import Tarea, Categoria, Comentario

admin.site.register(Tarea)
admin.site.register(Categoria)
admin.site.register(Comentario)