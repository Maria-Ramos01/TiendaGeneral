from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# ==========================================
# 1. MODELO DE TIENDA (Multitienda)
# ==========================================
class Tienda(models.Model):
    # Opciones desplegables para clasificar el tipo de tienda
    TIPO_TIENDA_CHOICES = [
        ('ropa', 'Tienda de Ropa'),
        ('lanas', 'Tienda de Lanas'),
        ('dulces', 'Tienda de Dulces'),
        ('general', 'Tienda General / Otra'),
    ]

    # Nombre comercial de la tienda
    nombre = models.CharField(max_length=100, unique=True)
    
    # Identificador amigable para URLs y carga de CSS/JS (ej: ropa, lanas, dulces)
    slug = models.SlugField(max_length=100, unique=True, help_text="Se usará para cargar el CSS/JS (ej: ropa, lanas, dulces)")
    
    # Descripción textual de la tienda (opcional)
    descripcion = models.TextField(blank=True, null=True)
    
    # Categoría principal de la tienda
    tipo = models.CharField(max_length=20, choices=TIPO_TIENDA_CHOICES, default='general')
    
    # Administrador Local asignado a esta tienda
    admin_local = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='tiendas_administradas',
        help_text="Usuario asignado como administrador de esta tienda específica"
    )
    
    # Estado de la tienda (activa/inactiva)
    activa = models.BooleanField(default=True)
    
    # Fecha de registro automática
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Tienda"
        verbose_name_plural = "Tiendas"

    def __str__(self):
        return f"{self.nombre} ({self.get_tipo_display()})"


# ==========================================
# 2. CATEGORÍAS DE PRODUCTOS
# ==========================================
class Categoria(models.Model):
    nombre = models.CharField(max_length=50)
    tienda = models.ForeignKey(Tienda, on_delete=models.CASCADE, related_name='categorias')

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        unique_together = ('nombre', 'tienda')

    def __str__(self):
        return f"{self.nombre} - {self.tienda.nombre}"


# ==========================================
# 3. MODELO DE PRODUCTO (Sin campo imagen)
# ==========================================
class Producto(models.Model):
    tienda = models.ForeignKey(Tienda, on_delete=models.CASCADE, related_name='productos')
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True, related_name='productos')
    
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    
    disponible = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

    def __str__(self):
        return f"{self.nombre} - ${self.precio} ({self.tienda.nombre})"


# ==========================================
# 4. CARRITO DE COMPRAS
# ==========================================
class Carrito(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_id = models.CharField(max_length=100, null=True, blank=True, help_text="Para usuarios no registrados")
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Carrito {self.id} - Usuario: {self.usuario or self.session_id}"

    @property
    def total(self):
        return sum(item.subtotal for item in self.items.all())


# ==========================================
# 5. ÍTEMS DEL CARRITO
# ==========================================
class ItemCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name='items')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    @property
    def subtotal(self):
        return self.producto.precio * self.cantidad

    def __str__(self):
        return f"{self.cantidad}x {self.producto.nombre}"