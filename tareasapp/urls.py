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
    
    # URLS FETCH PAGINAS
    path('tareas/',             views.inicio, name= 'inicio'),
    path('crear/',              views.crear_tarea, name= 'crear_tarea'),
    path('detalle/<int:id>/',   views.detalle_tarea, name= 'detalle_tarea'),
    path('editar/<int:id>/',    views.editar_tarea, name= 'editar_tarea'),
    path('eliminar/<int:id>/',  views.eliminar_tarea, name= 'eliminar_tarea'),

    # API AUTENTICACION
    path(
        'api/login/', 
        views.LoginAPIView.as_view(), 
        name= 'api_login'
    ),
    # API TAREAS
    path(
        'api/tareas/',
        views.TareasAPIView.as_view(),
        name = 'api_tareas'
    ),
    # API DEDICADA PARA DETALLE, EDITAR Y ELIMINAR TAREAS
    path(
        'api/tareas/<int:pk>/',
        views.TareaDetalleAPIView.as_view(),
        name = 'api_tarea_detalle'
    )
    # !!!!!!!!! puede...
    # puede que esto sea temporal
]