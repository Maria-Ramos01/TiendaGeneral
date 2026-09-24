// Obtiene el carrito del almacenamiento local
function getCart() {
    return JSON.parse(localStorage.getItem('cart')) || [];
}

// Guarda los cambios del carrito en localStorage y actualiza la vista
function saveCart(cart) {
    localStorage.setItem('cart', JSON.stringify(cart));
    updateCartUI();
}

// Agrega un producto al carrito
function addToCart(id, nombre, precio, tienda) {
    let cart = getCart();
    let existingItem = cart.find(item => item.id === id);

    if (existingItem) {
        existingItem.cantidad += 1;
    } else {
        cart.push({
            id: id,
            nombre: nombre,
            precio: parseFloat(precio),
            tienda: tienda || 'General',
            cantidad: 1
        });
    }

    saveCart(cart);
    openCart(); // Muestra el carrito lateral al agregar un objeto
}

// Elimina un objeto del carrito
function removeFromCart(id) {
    let cart = getCart();
    cart = cart.filter(item => item.id !== id);
    saveCart(cart);
}

// Actualiza la interfaz visual del carrito
function updateCartUI() {
    const cart = getCart();
    const cartCountEl = document.getElementById('cart-count');
    const cartItemsContainer = document.getElementById('cart-items-container');
    const cartTotalPriceEl = document.getElementById('cart-total-price');

    // Actualiza contador total
    const totalCount = cart.reduce((sum, item) => sum + item.cantidad, 0);
    if (cartCountEl) cartCountEl.innerText = totalCount;

    // Renderiza los objetos dentro del carrito deslizante
    if (cartItemsContainer) {
        if (cart.length === 0) {
            cartItemsContainer.innerHTML = '<p style="text-align:center; color:#888; margin-top:2rem;">El carrito está vacío.</p>';
        } else {
            cartItemsContainer.innerHTML = cart.map(item => `
                <div class="cart-item">
                    <div class="cart-item-info">
                        <h4>${item.nombre}</h4>
                        <p>$${item.precio.toLocaleString()} x ${item.cantidad}</p>
                        <small style="color:#888;">Tienda: ${item.tienda}</small>
                    </div>
                    <button onclick="removeFromCart('${item.id}')" style="background:none; border:none; color:#e74c3c; cursor:pointer; font-weight:bold;">✕</button>
                </div>
            `).join('');
        }
    }

    // Calcula y actualiza el total general
    const grandTotal = cart.reduce((sum, item) => sum + (item.precio * item.cantidad), 0);
    if (cartTotalPriceEl) {
        cartTotalPriceEl.innerText = `$${grandTotal.toLocaleString()}`;
    }
}

// Controla la visibilidad del panel lateral del carrito
function toggleCart() {
    const sidebar = document.getElementById('cart-sidebar');
    const overlay = document.getElementById('cart-overlay');
    if (sidebar && overlay) {
        sidebar.classList.toggle('open');
        overlay.classList.toggle('active');
    }
}

function openCart() {
    const sidebar = document.getElementById('cart-sidebar');
    const overlay = document.getElementById('cart-overlay');
    if (sidebar && overlay) {
        sidebar.classList.add('open');
        overlay.classList.add('active');
    }
}

document.addEventListener('DOMContentLoaded', updateCartUI);