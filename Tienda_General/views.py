from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.forms import AuthenticationForm
from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth import login, logout, authenticate

from .models import Tienda, Categoria, Producto, Carrito, ItemCarrito
from .serializer import (
    TiendaSerializer, 
    CategoriaSerializer, 
    ProductoSerializer, 
    CarritoSerializer, 
    ItemCarritoSerializer
)

# ==========================================
# VISTAS PARA RENDERIZAR TEMPLATES (HTML)
# ==========================================

def home_view(request):
    """
    Renderiza la página principal del Centro Comercial (home.html).
    """
    # Consulta 1: Obtiene únicamente las tiendas que estén marcadas como activas en la BD
    tiendas = Tienda.objects.filter(activa=True)
    
    # Consulta 2: Obtiene los productos disponibles que tengan stock mayor a 0 (limitado a los primeros 8 resultados con [:8])
    productos_destacados = Producto.objects.filter(disponible=True, stock__gt=0)[:8]
    
    # Diccionario que envía los datos consultados a la plantilla HTML
    context = {
        'tiendas': tiendas,
        'productos': productos_destacados
    }
    # Procesa y retorna la plantilla HTML 'marketplace/home.html' con las variables cargadas
    return render(request, 'marketplace/home.html', context)


def tienda_detail_view(request, slug):
    """
    Renderiza la vista propia de una tienda (ej: /tienda/ropa/ o /tienda/lanas/).
    """
    # Busca la tienda que coincida con el 'slug' enviado en la URL y esté activa.
    # Si no la encuentra, arroja un error 404 (Página no encontrada) automáticamente.
    tienda = get_object_or_404(Tienda, slug=slug, activa=True)
    
    # Obtiene todos los productos disponibles asociados específicamente a esta tienda
    productos = Producto.objects.filter(tienda=tienda, disponible=True)
    
    # Obtiene las categorías de productos pertenecientes a esta tienda
    categorias = Categoria.objects.filter(tienda=tienda)
    
    # Empaqueta las variables para pasarlas al HTML
    context = {
        'tienda': tienda,
        'productos': productos,
        'categorias': categorias
    }
    # Carga la plantilla común que usará el CSS y JS dinámico de la tienda según su slug
    return render(request, 'tiendas/tienda_detail.html', context)


def producto_detail_view(request, tienda_slug, producto_id):
    """
    Renderiza la página con el detalle de un único producto.
    """
    # Verifica que el producto exista por su ID, esté disponible y pertenezca a la tienda indicada por el slug
    producto = get_object_or_404(Producto, id=producto_id, tienda__slug=tienda_slug, disponible=True)
    
    # Pasa el objeto producto y su tienda correspondiente a la plantilla
    context = {
        'producto': producto,
        'tienda': producto.tienda
    }
    return render(request, 'tiendas/producto_detail.html', context)


def cart_view(request):
    """
    Renderiza la plantilla estática del carrito de compras (cart.html).
    Los datos del carrito se rellenarán dynamicamente en el cliente desde el navegador usando JS.
    """
    return render(request, 'marketplace/cart.html')


# ==========================================
# VISTAS DE API REST (Django REST Framework)
# ==========================================

class TiendaViewSet(viewsets.ModelViewSet):
    """
    ViewSet que gestiona las operaciones CRUD de las Tiendas en la API (/api/tiendas/).
    """
    # Define qué serializador usará para convertir objetos de Tienda a formato JSON
    serializer_class = TiendaSerializer
    
    # Permiso: Usuarios no autenticados solo pueden LEER (GET), usuarios autenticados pueden ESCRIBIR
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """
        Personaliza los datos devueltos según el rol del usuario que consulta la API.
        """
        user = self.request.user
        
        # 1. Si es Superusuario o Miembro del Staff (Admin General): Ve absolutamente TODAS las tiendas
        if user.is_staff or user.is_superuser:
            return Tienda.objects.all()
        
        # 2. Si es un Admin Local autenticado: Solo ve la tienda que le pertenece
        if user.is_authenticated:
            return Tienda.objects.filter(admin_local=user, activa=True)
        
        # 3. Si es un cliente o usuario anónimo: Solo ve las tiendas activas públicamente
        return Tienda.objects.filter(activa=True)


class CategoriaViewSet(viewsets.ModelViewSet):
    """
    ViewSet que gestiona las Categorías en la API (/api/categorias/).
    """
    serializer_class = CategoriaSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        
        # El Administrador General ve todas las categorías existentes
        if user.is_superuser:
            return Categoria.objects.all()
        
        # El Admin Local solo ve las categorías asociadas a su propia tienda
        if user.is_authenticated:
            return Categoria.objects.filter(tienda__admin_local=user)
        
        # Peticiones públicas leen todas las categorías
        return Categoria.objects.all()


class ProductoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para la consulta y administración de Productos (/api/productos/).
    Soporta filtrado dinámico en la URL (ej: /api/productos/?tienda_slug=ropa)
    """
    serializer_class = ProductoSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        # Base de la consulta: Solo productos habilitados
        queryset = Producto.objects.filter(disponible=True)
        
        # Captura si el usuario pasó el parámetro ?tienda_slug=... en la URL
        tienda_slug = self.request.query_params.get('tienda_slug', None)
        
        # Si se especificó una tienda en la URL, se filtran los productos de esa tienda únicamente
        if tienda_slug is not None:
            queryset = queryset.filter(tienda__slug=tienda_slug)
            
        user = self.request.user
        
        # Validación estricta para modificaciones: Si intenta CREAR, EDITAR o BORRAR un producto 
        # y es un Admin Local, restringe la acción para que solo afecte productos de su tienda
        if user.is_authenticated and not user.is_superuser and self.action in ['create', 'update', 'destroy']:
            return queryset.filter(tienda__admin_local=user)
            
        return queryset


class CarritoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para consultar y guardar carritos de compras (/api/carritos/).
    """
    serializer_class = CarritoSerializer
    # Permite acceso total (AllowAny) para que usuarios anónimos/invitados puedan crear su carrito
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        user = self.request.user
        
        # Si el usuario inició sesión, obtiene únicamente su carrito personal
        if user.is_authenticated:
            return Carrito.objects.filter(usuario=user)
        
        # Si es usuario no registrado, retorna todos los carritos (manejados por ID de sesión)
        return Carrito.objects.all()


class ItemCarritoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para agregar, modificar cantidades o borrar ítems específicos de un carrito.
    """
    serializer_class = ItemCarritoSerializer
    permission_classes = [permissions.AllowAny]
    
    # Retorna la lista completa de ítems para su manipulación directa
    queryset = ItemCarrito.objects.all()

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)  # Inicia sesión de sesión clásica de Django
            
            # Generar par de Tokens JWT para el cliente
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            
            # Guardar el token en la sesión de Django
            request.session['access_token'] = access_token
            request.session['refresh_token'] = str(refresh)

            messages.success(request, f"¡Bienvenido, {user.username}!")
            return redirect('home')
        else:
            messages.error(request, "Usuario o contraseña incorrectos.")
    else:
        form = AuthenticationForm()

    return render(request, 'marketplace/login.html', {'form': form})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def realizar_compra_api(request):
    """Ejemplo de Endpoint protegido exclusivamente por JWT"""
    usuario = request.user
    # Lógica de procesamiento del carrito y compra...
    return Response({
        "mensaje": f"Compra procesada con éxito para {usuario.username}",
        "estado": "completado"
    })