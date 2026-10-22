
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate

from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import Tarea

# Create your views here.

# Esta es la logica de toda la aplicaicon

def inicio(request):
    tareas = Tarea.objects.all()

    return render(request, 'tareasapp/inicio.html', {
        'tareas': tareas
    }) 

def crear_tarea(request):
    if request.method == 'POST':
        titulo = request.POST['titulo']
        descripcion = request.POST['descripcion']
        completada = 'completada' in request.POST

        Tarea.objects.create(
            titulo = titulo,
            descripcion = descripcion,
            completada = completada
        )

        return redirect('inicio')
        # LLEVA AL INICIO
    return render (request, 'tareasapp/crear.html')

# MOSTRAR URL DE DETALLE TAREA CON LA ID DE LA TAREA
# A DETALLAR
def detalle_tarea(request, id):
    tarea = Tarea.objects.get(id=id)
    
    return render(request, 'tareasapp/detalle.html', {
        'tarea': tarea
    })

# EDITAR TAREA CON EL ID
def editar_tarea(request, id):
    tarea = Tarea.objects.get(id=id)
    
    if request.method == 'POST':
        tarea.titulo = request.POST['titulo']
        tarea.descripcion = request.POST['descripcion']
        # LOS TRUEFALSE SIEMPRE EMPIEZAN EN FALSO
        tarea.completada = 'completada' in request.POST
        tarea.save()
        return redirect('inicio')
    
    return render(request, 'tareasapp/editar.html', {
        'tarea' : tarea
    })

def eliminar_tarea(request, id):
    tarea = Tarea.objects.get(id=id)

    if request.method == 'POST':
        tarea.delete()
        return redirect('inicio')
    
    return render(request, 'tareasapp/eliminar.html', {
        'tarea': tarea
    })

def login_pagina(request):
    
    return render(request, 'tareasapp/login.html')

# API DE LOGIN
class LoginAPIView(APIView):

    # NSE QUE HACE ESTO
    permission_classes = [AllowAny]

    def post(self, request):
        # ESTO LO DA EL SCRIPT DE LOGIN.HTML
        username = request.data.get('username')
        password = request.data.get('password')

        # VALIDAR
        usuario = authenticate(
            username=username,
            password=password
        )
        # Si existen las credenciales del usuario
        # significa que si esta valido
        if usuario is not None:
            token, creado = Token.objects.get_or_create(
                user=usuario
            )
            # CREAR TOKEN Y DEVOLVER LA LLAVE DEL TOKEN
            return Response(
                {
                    'mensaje' : 'Autenticado',
                    'usuario' : usuario.username,
                    'token': token.key
                },
                status=status.HTTP_200_OK
            )
        # no pasa nada tio
        return Response(
            {
                'error' : 'Usuario o contraseña incorrecta',
            },
            status=status.HTTP_401_UNAUTHORIZED
        )

# API DE TAREAS
class TareasAPIView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # GET LIST TAREAS
    def get(self, request):

        tareas = Tarea.objects.all()
        datos = []

        for tarea in tareas:
            datos.append({
                'id': tarea.id,
                'titulo': tarea.titulo,
                'descripcion' : tarea.descripcion,
                'completada' : tarea.completada
            })
            
        return Response(datos, status.HTTP_200_OK)

    pass