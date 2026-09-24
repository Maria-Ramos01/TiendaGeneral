from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Tienda, Categoria, Producto, Carrito, ItemCarrito

# serializer.py es el puente de comunicación en Django REST Framework (DRF) que traduce los datos entre la base de datos de Python 
# y el formato JSON que entienden las aplicaciones web, móviles o scripts JavaScript.

# ==========================================
# 1. SERIALIZADOR DE USUARIOS (Para ver info del Admin Local)
# ==========================================
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # Exponemos solo los datos públicos necesarios del usuario
        fields = ['id', 'username', 'email']


# ==========================================
# 2. SERIALIZADOR DE TIENDAS
# ==========================================
class TiendaSerializer(serializers.ModelSerializer):
    # Muestra el nombre legible del tipo de tienda (ej: "Tienda de Ropa" en vez de "ropa")
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    
    # Anidamos los datos del admin local utilizando el UserSerializer definido arriba
    admin_local_detail = UserSerializer(source='admin_local', read_only=True)

    class Meta:
        model = Tienda
        fields = [
            'id', 
            'nombre', 
            'slug', 
            'descripcion', 
            'tipo', 
            'tipo_display', 
            'admin_local', 
            'admin_local_detail', 
            'activa', 
            'fecha_creacion'
        ]


# ==========================================
# 3. SERIALIZADOR DE CATEGORÍAS
# ==========================================
class CategoriaSerializer(serializers.ModelSerializer):
    # Incluye el nombre de la tienda asociada
    tienda_nombre = serializers.ReadOnlyField(source='tienda.nombre')

    class Meta:
        model = Categoria
        fields = ['id', 'nombre', 'tienda', 'tienda_nombre']


# ==========================================
# 4. SERIALIZADOR DE PRODUCTOS
# ==========================================
class ProductoSerializer(serializers.ModelSerializer):
    # Campos informativos de lectura para obtener datos de las relaciones ForeignKey
    tienda_nombre = serializers.ReadOnlyField(source='tienda.nombre')
    tienda_slug = serializers.ReadOnlyField(source='tienda.slug')
    categoria_nombre = serializers.ReadOnlyField(source='categoria.nombre', default=None)

    class Meta:
        model = Producto
        fields = [
            'id', 
            'tienda', 
            'tienda_nombre', 
            'tienda_slug', 
            'categoria', 
            'categoria_nombre', 
            'nombre', 
            'descripcion', 
            'precio', 
            'stock', 
            'disponible', 
            'fecha_creacion'
        ]


# ==========================================
# 5. SERIALIZADOR DE ÍTEMS DE CARRITO
# ==========================================
class ItemCarritoSerializer(serializers.ModelSerializer):
    # Incluye la información detallada del producto dentro del ítem
    producto_detail = ProductoSerializer(source='producto', read_only=True)
    
    # Campo calculado (@property del modelo): multiplica precio * cantidad
    subtotal = serializers.ReadOnlyField()

    class Meta:
        model = ItemCarrito
        fields = ['id', 'carrito', 'producto', 'producto_detail', 'cantidad', 'subtotal']


# ==========================================
# 6. SERIALIZADOR DE CARRITO COMPLETO
# ==========================================
class CarritoSerializer(serializers.ModelSerializer):
    # Muestra la lista de todos los ítems dentro de este carrito
    items = ItemCarritoSerializer(many=True, read_only=True)
    
    # Campo calculado (@property del modelo): suma el subtotal de todos sus ítems
    total = serializers.ReadOnlyField()

    class Meta:
        model = Carrito
        fields = ['id', 'usuario', 'session_id', 'items', 'total', 'fecha_creacion']