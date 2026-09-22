// Lógica interactiva específica para la tienda de dulces
document.addEventListener('DOMContentLoaded', () => {
console.log('Módulo de tienda de dulces cargado.');
initCandyEffects();
});

function initCandyEffects() {
const container = document.getElementById('tienda-custom-options');
if (!container) return;

container.innerHTML = `
    <div style="margin: 1rem 0; background: #fff; padding: 10px; border-radius: 10px; border: 1px dashed #ff4081;">
        <p>🍬 <strong>¡Dulce Sorpresa!</strong> Cada pedido incluye stickers coleccionables gratis.</p>
    </div>
`;


}

// Sobrescribir / extender la función de agregar para efectos festivos
const originalAddToCart = window.addToCart;
window.addToCart = function(id, nombre, precio, tienda) {
if (typeof originalAddToCart === 'function') {
originalAddToCart(id, nombre, precio, tienda);
}
alert('🎉 ¡Mmm! Agregaste algo súper dulce a tu carrito.');
};