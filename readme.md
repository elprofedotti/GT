#  📝 Gestarea

Gestarea es una aplicación web de gestión de tareas desarrollada con Django y MySQL. Permite a los usuarios crear, editar y gestionar tareas, así como comentarlas. Las tareas se pueden categorizar para una fácil clasificaci贸n y búsqueda.

##  🚀 Empezando

Estas instrucciones te permitirán obtener una copia del proyecto en funcionamiento en tu máquina local para propósitos de desarrollo y pruebas.

###  📋 Prerrequisitos

Para ejecutar este proyecto, necesitarás tener instalado Python 3.8 (o superior) y pip..

###  📥 Instalación

1. Clona este repositorio en tu máquina local.:

   ```
   git clone https://github.com/elprofedotti/gestarea
   ```
   🔄 Configurar tu Propio Repositorio
   Si planeas hacer cambios en el proyecto y subirlos a tu propio repositorio (GitHub, Bitbucket, etc) es recomendable que configures tu "fork" del repositorio original.
        
2. Navega al directorio del proyecto:
   (Suponiendo creaste la carpeta gestarea, y clonaste ahi el repo)
   ```
   cd gestarea
   ```

3. Crea un entorno virtual:

   ```
   python -m venv env
   ```

	- env: "nombre del entorno que quieras darle"
	
	
4. Activa el entorno virtual:

   - En Windows:

     ```
     env\Scripts\activate
     ```

   - En macOS/Linux:

     ```
     source env/bin/activate
     ```

5. Instala las dependencias del proyecto:
   (debes estar dentro de la carpeta p_gestarea.)

   ```
   pip install -r requerimientos.txt
   ```

6. Descripcion de Clases:

- `Categoria` con un campo `nombre`.
- `Tarea` con campos `nombre`, `descripcion`, `fecha_vencimiento`, `estado`, `prioridad`, `categoria` (que es una relación con `Categoria`), y `asignada_a` (que es una relaci贸n con `Usuario`).
- `Comentario` con campos `texto`, `creado_por` (que es una relación con `Usuario`), `tarea` (que es una relaci贸n con `Tarea`), y `visibilidad`.

7. Ejecuta las migraciones de Django:

   ```
   python manage.py migrate
   ```

8. Ejecuta el servidor de desarrollo de Django:

   ```
   python manage.py runserver
   ```



Ahora deberías poder acceder a la aplicación en `http://localhost:8000/login`.

## 📦 Despliegue

Para desplegar la aplicación, consulta la [documentación de Django](https://docs.djangoproject.com/en/3.1/howto/deployment/) para obtener instrucciones.

## 🛠️ Construido con

- [`Django`](https://www.djangoproject.com/) - Framework usado
- `SQLite` BD usada

## 🖋️ Autores

- **Maximiliano Gauthier**
- **Rocío Leggerini**
- **Joaquin Lopes**
- **Matías Dotti**

---

# 👥Contribuir

Si quieres contribuir a este proyecto, sigue estos pasos:

1. Haz un "Fork" del repositorio. Esto creará una copia del repositorio en tu cuenta.

2. Clona tu "fork" en tu máquina local:

    ```bash
    git clone https://github.com/<tu-nombre-de-usuario>/gestarea
    ```
	
3. Configura el repositorio original como un "upstream" remoto:

    ```bash
    cd gestarea
    git remote add upstream https://github.com/elprofedotti/gestarea
    ```
	

4. Crea una nueva rama para tus cambios:

    ```bash
    git checkout -b nombre-de-tu-rama
    ```

5. Realiza tus cambios y haz "commit" a ellos en tu rama.

6. Haz "push" de tu rama a tu "fork":

    ```bash
    git push origin nombre-de-tu-rama
    ```

7. Ve a la página de tu "fork", y haz clic en "New Pull Request". Selecciona tu rama en el desplegable y haz clic en "Create Pull Request".



