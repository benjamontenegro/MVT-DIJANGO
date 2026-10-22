from django.urls import path
from . import views

# RUTAS CON SUS FUNCIONES  Y TOA LA WEA
# ASKBAKSBDASKDB

urlpatterns = [
    # path(
    #     '', 
    #     views.inicio, 
    #     name= 'inicio'
    # ),
    path(
        '', 
        views.login_pagina, 
        name= 'login_pagina'
    ),
    
    # PAGINAS
    path(
        'tareas/', 
        views.inicio, 
        name= 'inicio'
    ),
    path(
        'crear/', 
        views.crear_tarea, 
        name= 'crear_tarea'
    ),
    path(
        'detalle/<int:id>/',
        views.detalle_tarea, 
        name= 'detalle_tarea'
    ),
    path(
        'editar/<int:id>/',
        views.editar_tarea,
        name= 'editar_tarea'
    ),
    path(
        'eliminar/<int:id>/',
        views.eliminar_tarea,
        name= 'eliminar_tarea'
    ),

    # API AUTENTICACION
    path(
        'api/login/', 
        views.LoginAPIView.as_view(), 
        name= 'api_login'
    ),
    # API LISTAR TAREAS
    path(
        'api/tareas/',
        views.TareasAPIView.as_view(),
        name = 'api_tareas'
    )
]