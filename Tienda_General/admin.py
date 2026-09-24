from django.contrib import admin
from .models import Tienda, Categoria, Producto, Carrito, ItemCarrito

@admin.register(Tienda)
class TiendaAdmin(admin.ModelAdmin):
    # Cambiamos 'propietario' por 'admin_local'
    list_display = ('nombre', 'slug', 'admin_local', 'tipo', 'activa')
    list_filter = ('tipo', 'activa')
    search_fields = ('nombre', 'admin_local__username')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Si es Superusuario (Admin General), ve todas las tiendas
        if request.user.is_superuser:
            return qs
        # Si es admin local, solo ve las tiendas donde está asignado
        return qs.filter(admin_local=request.user)


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tienda')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(tienda__admin_local=request.user)


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tienda', 'precio', 'stock', 'disponible')
    list_filter = ('tienda', 'disponible')
    search_fields = ('nombre',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(tienda__admin_local=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Filtra las opciones del desplegable para que el admin local solo pueda asociar sus propias tiendas
        if db_field.name == "tienda" and not request.user.is_superuser:
            kwargs["queryset"] = Tienda.objects.filter(admin_local=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Carrito)
class CarritoAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'session_id', 'fecha_creacion')


@admin.register(ItemCarrito)
class ItemCarritoAdmin(admin.ModelAdmin):
    list_display = ('carrito', 'producto', 'cantidad', 'subtotal')