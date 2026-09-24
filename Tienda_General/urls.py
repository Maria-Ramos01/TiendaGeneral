from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# ==========================================
# 1. CONFIGURACIÓN DEL ROUTER (Django REST Framework)
# ==========================================
# Instanciamos el DefaultRouter, que crea automáticamente la lista de URLs estándar
# para un CRUD completo (GET, POST, PUT, DELETE) según las vistas (ViewSets) registradas.
router = DefaultRouter()

# Registra la ruta base '/api/tiendas/' para consultar, crear o editar tiendas
# 'basename' asigna un nombre interno para identificar este grupo de rutas en la API
router.register(r'tiendas', views.TiendaViewSet, basename='api-tiendas')

# Registra la ruta base '/api/categorias/' para las categorías de cada tienda
router.register(r'categorias', views.CategoriaViewSet, basename='api-categorias')

# Registra la ruta base '/api/productos/' (permite filtrar productos por parámetros de URL)
router.register(r'productos', views.ProductoViewSet, basename='api-productos')

# Registra la ruta base '/api/carritos/' para gestionar carritos de compra de clientes
router.register(r'carritos', views.CarritoViewSet, basename='api-carritos')

# Registra la ruta base '/api/items-carrito/' para añadir/modificar los elementos dentro de un carrito
router.register(r'items-carrito', views.ItemCarritoViewSet, basename='api-items-carrito')


# ==========================================
# 2. DEFINICIÓN DE RUTAS (urlpatterns)
# ==========================================
urlpatterns = [
    # --- RUTAS DE VISTAS HTML (Renderizan plantillas .html) ---
    
    # Vista principal (Home): Muestra el portal del centro comercial
    path('', views.home_view, name='home'),
    
    # Vista del Carrito: Muestra la pantalla general de compras seleccionadas
    path('carrito/', views.cart_view, name='cart'),
    
    # Vista de Tienda Individual: Captura el 'slug' (ej: /tienda/ropa/ o /tienda/dulces/) 
    # para renderizar la tienda correspondiente con su CSS y JS específico
    path('tienda/<slug:slug>/', views.tienda_detail_view, name='tienda_detail'),
    
    # Vista de Detalle de Producto: Recibe el 'slug' de la tienda y el 'ID' del producto 
    # (ej: /tienda/lanas/producto/12/)
    path('tienda/<slug:tienda_slug>/producto/<int:producto_id>/', views.producto_detail_view, name='producto_detail'),


    # --- RUTAS DE LA API REST ---
    
    # Incluye todas las URLs generadas dinámicamente por el 'router'
    # Las peticiones comenzarán con '/api/' (ej: /api/tiendas/, /api/productos/, etc.)
    path('api/', include(router.urls)),
]