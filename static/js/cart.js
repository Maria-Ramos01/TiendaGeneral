function getCart() {
    return JSON.parse(localStorage.getItem('cart')) || [];
}

function addToCart(id, nombre, precio) {
    let cart = getCart();
    let existing = cart.find(item => item.id === id);

    if (existing) {
        existing.cantidad += 1;
    } else {
        cart.push({ id: id, nombre: nombre, precio: precio, cantidad: 1 });
    }

    localStorage.setItem('cart', JSON.stringify(cart));
    updateCartCount();
    alert(`${nombre} fue agregado al carrito.`);
}

function updateCartCount() {
    let cart = getCart();
    let totalItems = cart.reduce((sum, item) => sum + item.cantidad, 0);
    const cartCountEl = document.getElementById('cart-count');
    if (cartCountEl) {
        cartCountEl.innerText = totalItems;
    }
}

document.addEventListener('DOMContentLoaded', updateCartCount);