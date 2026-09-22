from django.contrib import admin
from .models import Tienda, Producto

# Register your models here.

@admin.register(Tienda)
class TiendaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'slug', 'propietario')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Si es superusuario (Admin General), ve todas las tiendas
        if request.user.is_superuser:
            return qs
        # Si es admin local, solo ve su propia tienda
        return qs.filter(propietario=request.user)


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tienda', 'precio')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(tienda__propietario=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Limita la selección de tiendas al crear productos si no es superusuario
        if db_field.name == "tienda" and not request.user.is_superuser:
            kwargs["queryset"] = Tienda.objects.filter(propietario=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)