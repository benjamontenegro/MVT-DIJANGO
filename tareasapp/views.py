
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

def inicio(request):
    # tareas = Tarea.objects.all()

    return render(request, 'tareasapp/inicio.html') 


def crear_tarea(request):
    # !!!!! YA NO SE OCUPA, SOLO SE USA PARA MOSTRAR LA PAGINA

    # if request.method == 'POST':
    #     titulo = request.POST['titulo']
    #     descripcion = request.POST['descripcion']
    #     completada = 'completada' in request.POST

    #     Tarea.objects.create(
    #         titulo = titulo,
    #         descripcion = descripcion,
    #         completada = completada
    #     )

    #     return redirect('inicio')
    #     # LLEVA AL INICIO
    return render (request, 'tareasapp/crear.html')

# MOSTRAR URL DE DETALLE TAREA CON LA ID DE LA TAREA
# A DETALLAR
def detalle_tarea(request, id):
    # tarea = Tarea.objects.get(id=id)
    
    return render(request, 'tareasapp/detalle.html'
    # , { 'tarea': tarea}
    )

# EDITAR TAREA CON EL ID
def editar_tarea(request, id):
    # tarea = Tarea.objects.get(id=id)
    
    # if request.method == 'POST':
    #     tarea.titulo = request.POST['titulo']
    #     tarea.descripcion = request.POST['descripcion']
    #     # LOS TRUEFALSE SIEMPRE EMPIEZAN EN FALSO
    #     tarea.completada = 'completada' in request.POST
    #     tarea.save()
    #     return redirect('inicio')
    
    return render(request, 'tareasapp/editar.html'
    # , {'tarea' : tarea}
    )

def eliminar_tarea(request, id):
    # tarea = Tarea.objects.get(id=id)

    # if request.method == 'POST':
    #     tarea.delete()
    #     return redirect('inicio')
    
    return render(request, 'tareasapp/eliminar.html'
    # , { 'tarea': tarea}
    )

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

    # ESTE ES IMPORTANTE. SIGNIFICA QUE PERMISOS PIDE
    # PARA APLICAR EL METODO
    permission_classes = [IsAuthenticated]
    # IsAuthenticated -> SOLO CON AUTENTICACION
    # AllowAny -> PERMITE CUALQUIERA

    ##############################################################################
    # LISTAR TAREAS
    def get(self, request):

        tareas = Tarea.objects.all() # !!!!!!!!!!!!!!!!
        datos = []

        for tarea in tareas:
            datos.append({
                'id': tarea.id,
                'titulo': tarea.titulo,
                'descripcion' : tarea.descripcion,
                'completada' : tarea.completada
            })
        
        return Response(datos, status.HTTP_200_OK)
        # OSEA QUE LA RESPONSE ENVIA TODOS LOS 
        # DATOS PEDIDOS LOS DATOS DE LA TABLA 'tareas'
        # Y TAMBIEN UN ESTATUS DE LA CONSULTA
    pass

    ##############################################################################
    # POST: Crear una nueva tarea
    def post(self, request):
        # JIJIJ ESTO ME LO DIO LA IA (｡◕‿‿◕｡)

        # Usamos request.data porque DRF procesa automáticamente el JSON enviado desde el fetch
        # no tengo chucha idea que significa DRF
        titulo = request.data.get('titulo')
        descripcion = request.data.get('descripcion')
        completada = request.data.get('completada', False)

        # Validación básica opcional
        # if not titulo:
        #     return Response({'error': 'El título es obligatorio'}, status=status.HTTP_400_BAD_REQUEST)

        # EL TEMPLATE YA PIDE LOS CAMPOS

        # Crear la tarea en la base de datos
        tarea = Tarea.objects.create(
            titulo=titulo,
            descripcion=descripcion,
            completada=completada
        )

        # Devolver la respuesta con los datos creados y un status 201 (Created)
        return Response({
            'id': tarea.id,
            'titulo': tarea.titulo,
            'descripcion': tarea.descripcion,
            'completada': tarea.completada
        }, status=status.HTTP_201_CREATED)


# API PARA TAREAS CON ID ESPECIFICA
class TareaDetalleAPIView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    ##############################################################################
    # FUNCION PARA TAREAS CON X ID
    def get_object(self, pk):
        try:
            return Tarea.objects.get(pk=pk) # !!!!!!!!!!!!!!!!!!!
        except Tarea.DoesNotExist:
            return None

    ##############################################################################
    # GET TAREAS (ID)
    def get(self, request, pk):

        tarea = self.get_object(pk)

        # SI NO EXISTE, DEVUELVE UN ERROR NOMAS YERA
        if not tarea:
            return Response({
                'error': 'No existe la tarea solicitada...'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # SI EXISTE, DEVUELVE LA TAREA ESPECIFICA
        return Response({
            'id': tarea.id,
            'titulo': tarea.titulo,
            'descripcion': tarea.descripcion,
            'completada': tarea.completada
        }, status=status.HTTP_200_OK)
        pass

    ##############################################################################
    # UPDATE FULL TAREA
    def put(self, request, pk):

        tarea = self.get_object(pk)

        # SI NO EXISTE, DEVUELVE UN ERROR NOMAS YERA
        if not tarea:
            return Response({
                'error': 'No existe la tarea solicitada...'},
                status=status.HTTP_404_NOT_FOUND
            )

        titulo = request.data.get('titulo')
        descripcion = request.data.get('descripcion')
        completada = request.data.get('completada', False)

        # OTRO ERROR, POR MAL ESCRITURA (puede q este no vaya)
        if not titulo or not descripcion:
            return Response({
                'error': 'El título y la descripción son obligatorios'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # hasta este punto ya es lo mismo del create no?
        # bueno tmbn tiene cosas del view original de editar
        tarea.titulo = titulo
        tarea.descripcion = descripcion
        tarea.completada = completada
        tarea.save()

        # DEVUELVE LA TAREA
        return Response({
            'id': tarea.id,
            'titulo': tarea.titulo,
            'descripcion': tarea.descripcion,
            'completada': tarea.completada
        }, status=status.HTTP_200_OK)
        pass

    ##############################################################################
    # METODO PATCH
    # tengo que comentar este
    def patch(self, request, pk):
        
        tarea = self.get_object(pk)
        if not tarea:
            return Response({
                'error': 'Tarea no encontrada'}, 
                status=status.HTTP_404_NOT_FOUND
            )

        # si no estan todos los datos editados
        # como en el put
        # solo edita algunos datos 
        if 'titulo' in request.data:
            tarea.titulo = request.data.get('titulo')
        if 'descripcion' in request.data:
            tarea.descripcion = request.data.get('descripcion')
        if 'completada' in request.data:
            tarea.completada = request.data.get('completada')
        tarea.save()

        return Response({
            'id': tarea.id,
            'titulo': tarea.titulo,
            'descripcion': tarea.descripcion,
            'completada': tarea.completada
        }, status=status.HTTP_200_OK)

    ##############################################################################
    # METODO DELETE
    def delete(self, request, pk):

        tarea = self.get_object(pk)
        if not tarea:
            return Response({
                'error': 'Tarea no encontrada'}, 
                status=status.HTTP_404_NOT_FOUND
            )

        tarea.delete()
        # no content pq ya no hay content cffffffffffffffffffff
        return Response(status=status.HTTP_204_NO_CONTENT)

# hermano de toda esta mierda, nada lo iba a inventar yo solo
# lit estaba hecho para que lo pusiera en la ia y me diera resultados
# soy re flojo askdaksdkajsdh
# bueno igual no fui a esas clases xd