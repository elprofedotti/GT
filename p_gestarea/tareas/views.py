from django.shortcuts import render, get_object_or_404, redirect # type: ignore
from .models import Tarea, Comentario, Categoria
from django.contrib.auth.models import User # type: ignore
from django.contrib.auth import authenticate, login # type: ignore
from django.contrib.auth.forms import UserCreationForm # type: ignore
from .forms import CambioTareaForm, TareaForm, TareaFormAdmin
from django.db import connection # type: ignore
from django.db.models import Q # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore

	
def inicio(request):
    if not request.user.is_authenticated:
        return redirect('inicio_sesion')
        
    if request.user.is_superuser:
        # plantilla de inicio para administrador.
        categorias = Categoria.objects.all()
        tareas = Tarea.objects.all().count()
        tareas_pendientes = Tarea.objects.filter(estado='PENDIENTE')
        tareas_en_progreso = Tarea.objects.filter(estado='EN_PROGRESO')
        tareas_completadas = Tarea.objects.filter(estado='COMPLETADA')
        tareas_pendientes_tot = Tarea.objects.filter(estado='PENDIENTE').count()
        tareas_en_progreso_tot = Tarea.objects.filter(estado='EN_PROGRESO').count()
        tareas_completadas_tot = Tarea.objects.filter(estado='COMPLETADA').count()
        usuarios = User.objects.all()
        
        context = {
        'categorias': categorias,
        'tareas_tot': tareas,
		'tareas_pendientes': tareas_pendientes,
        'tareas_en_progreso': tareas_en_progreso,
        'tareas_completadas': tareas_completadas,
        'tareas_pendientes_tot': tareas_pendientes_tot,
        'tareas_en_progreso_tot': tareas_en_progreso_tot,
        'tareas_completadas_tot': tareas_completadas_tot,
		'usuarios': usuarios
        }
        return render(request, 'inicio.html', context)
    else:
        # plantilla de inicio para usuarios comunes

        usuario_actual = User.objects.get(username=request.user.username)

        tareas_publicas = [(tarea, CambioTareaForm(initial={'estado': tarea.estado})) for tarea in Tarea.objects.filter(es_publica=True)]
    
        tareas_privadas = [(tarea, CambioTareaForm(initial={'estado': tarea.estado})) for tarea in Tarea.objects.filter(es_publica=False, asignada_a=usuario_actual)]
        
        context = {
        'tareas_publicas': tareas_publicas,
        'tareas_privadas': tareas_privadas,
        }
        return render(request, 'tareas/inicio.html', context)



def lista_tareas(request):
    tareas = Tarea.objects.all()
    return render(request, 'tareas/lista_tareas.html', {'tareas': tareas})

def detalle_tarea(request, id_tarea):
    tarea = get_object_or_404(Tarea, id=id_tarea)
    return render(request, 'tareas/detalle_tarea.html', {'tarea': tarea})

def cambiar_estado_tarea(request, tarea_id):
    # Comprobar si el usuario está autenticado
    if not request.user.is_authenticated:
        return HttpResponseForbidden('No tienes permiso para realizar esta acción.') # type: ignore

    usuario_actual = request.user
	
    if request.method == 'POST':
        form = CambioTareaForm(request.POST)
        if form.is_valid():
            estado = form.cleaned_data['estado']
            comentario_texto = form.cleaned_data['comentario']
            visibilidad = form.cleaned_data['visibilidad']

            tarea = get_object_or_404(Tarea, pk=tarea_id)
			
            usuario_actual = User.objects.get(username=request.user.username)

            # Cambio estado de tarea y, si es pública, asigno al usuario actual
            tarea.estado = estado
            if tarea.es_publica:
                tarea.asignada_a = usuario_actual
            tarea.save()

            # Si se agrego comentario, lo agrego
            if comentario_texto:
                comentario = Comentario(
                    texto=comentario_texto,
                    creado_por=usuario_actual,
                    tarea=tarea,
                    visibilidad=visibilidad
                )
                comentario.save()

            return redirect('inicio')
    else:
        return HttpResponseNotAllowed(['POST']) # type: ignore

		
def lista_categorias(request):
    categorias = Categoria.objects.all()
    return render(request, 'tareas/lista_categorias.html', {'categorias': categorias})
	
def lista_usuarios(request):
    usuarios = User.objects.all()
    return render(request, 'tareas/lista_usuarios.html', {'usuarios': usuarios})

def lista_comentarios(request):
    comentarios = Comentario.objects.all()
    return render(request, 'tareas/lista_comentarios.html', {'comentarios': comentarios})

def registro_usuario(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inicio_sesion')
    else:
        form = UserCreationForm()
    return render(request, 'tareas/registro_usuario.html', {'form': form})

def inicio_sesion(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('inicio')
        else:
            # código si falla inicio de sesión
            pass
    else:
        return render(request, 'tareas/inicio_sesion.html')

def admin(request):
    return render(request, 'admin/')
	
def chau(request):
	return render(request, 'tareas/inicio.html')
	
def agregar_tarea(request):
    if not request.user.is_authenticated:
        return redirect('inicio_sesion')
    
    if request.method == 'POST':
        form = TareaForm(request.POST)
        if form.is_valid():
            nueva_tarea = form.save(commit=False)
            nueva_tarea.asignada_a = request.user  # Se asigna la tarea al usuario actual
            nueva_tarea.save()
            return redirect('inicio')
    else:
        form = TareaForm()
    
    return render(request, 'tareas/agregar_tarea.html', {'form': form})
    
def agregar_tareaSQL(request):
    if not request.user.is_authenticated:
        return redirect('inicio_sesion')
    
    if request.method == 'POST':
        form = TareaForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            descripcion = form.cleaned_data['descripcion']
            fecha_vencimiento = form.cleaned_data['fecha_vencimiento']
            estado = form.cleaned_data['estado']
            prioridad = form.cleaned_data['prioridad']
            categoria_id = form.cleaned_data['categoria'].id
            es_publica = form.cleaned_data['es_publica']
            asignada_a_id = request.user.id

            with connection.cursor() as cursor:
                cursor.execute('''
                    INSERT INTO tareas_tarea (nombre, descripcion, fecha_vencimiento, estado, prioridad, categoria_id, asignada_a_id, es_publica)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ''', [nombre, descripcion, fecha_vencimiento, estado, prioridad, categoria_id, asignada_a_id, es_publica])
            
            return redirect('inicio')
    else:
        form = TareaForm()
    
    return render(request, 'tareas/agregar_tareaSQL.html', {'form': form})
    
def agregar_tarea_admin(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect('inicio_sesion')
    
    if request.method == 'POST':
        form = TareaFormAdmin(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            descripcion = form.cleaned_data['descripcion']
            fecha_vencimiento = form.cleaned_data['fecha_vencimiento']
            estado = form.cleaned_data['estado']
            prioridad = form.cleaned_data['prioridad']
            categoria_id = form.cleaned_data['categoria'].id
            es_publica = form.cleaned_data['es_publica']
            asignada_a_id = form.cleaned_data['asignada_a'].id

            with connection.cursor() as cursor:
                cursor.execute('''
                    INSERT INTO tareas_tarea (nombre, descripcion, fecha_vencimiento, estado, prioridad, categoria_id, asignada_a_id, es_publica)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ''', [nombre, descripcion, fecha_vencimiento, estado, prioridad, categoria_id, asignada_a_id, es_publica])
            
            return redirect('inicio')
    else:
        form = TareaFormAdmin()
    
    return render(request, 'tareas/agregar_tarea_admin.html', {'form': form})
    
@login_required
def eliminar_tarea(request, id_tarea):
    tarea = get_object_or_404(Tarea, id=id_tarea)
    if request.method == 'POST':
        tarea.delete()
        return redirect('lista_tareas')
    return render(request, 'tareas/eliminar_tarea_confirmacion.html', {'tarea': tarea})
