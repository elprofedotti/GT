#los "endpoints!"
from django.urls import path  # type: ignore
from django.contrib.auth.views import LogoutView # type: ignore
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('inicio', views.inicio, name='inicio'),
    path('tareas/', views.lista_tareas, name='lista_tareas'),
    path('tareas/<int:id_tarea>/', views.detalle_tarea, name='detalle_tarea'),
    path('cambiar_estado_tarea/<int:tarea_id>/', views.cambiar_estado_tarea, name='cambiar_estado_tarea'),
    path('categorias/', views.lista_categorias, name='lista_categorias'),
	path('comentarios/', views.lista_comentarios, name='lista_comentarios'),
	path('usuarios/', views.lista_usuarios, name='lista_usuarios'),
    path('registro/', views.registro_usuario, name='registro_usuario'),
    path('login/', views.inicio_sesion, name='inicio_sesion'),
	path('admin/', views.inicio_sesion, name='admin'),
    path('logout/', LogoutView.as_view(), name='logout'),
	path('chau/', views.chau, name='chau'),
	path('agregar_tarea/', views.agregar_tarea, name='agregar_tarea'),
	path('agregar_tareaSQL/', views.agregar_tareaSQL, name='agregar_tareaSQL'),
	 path('agregar_tarea_admin/', views.agregar_tarea_admin, name='agregar_tarea_admin'), 
]
