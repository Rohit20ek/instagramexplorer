// Initialize Lucide Icons
lucide.createIcons();

// State
let cart = [];

// DOM Elements
const cartBtn = document.getElementById('open-cart-btn');
const closeCartBtn = document.getElementById('close-cart-btn');
const cartOverlay = document.getElementById('cart-overlay');
const cartSidebar = document.getElementById('cart-sidebar');
const cartBadge = document.getElementById('cart-badge');
const cartItemsContainer = document.getElementById('cart-items');
const cartTotalPrice = document.getElementById('cart-total-price');
const checkoutBtn = document.getElementById('checkout-btn');
const toastContainer = document.getElementById('toast-container');

// Event Listeners for Cart Sidebar
cartBtn.addEventListener('click', toggleCart);
closeCartBtn.addEventListener('click', toggleCart);
cartOverlay.addEventListener('click', toggleCart);

function toggleCart() {
    cartSidebar.classList.toggle('active');
    cartOverlay.classList.toggle('active');
}

// Add to Cart Functionality
const addToCartBtns = document.querySelectorAll('.add-to-cart, #hero-add-to-cart');

addToCartBtns.forEach(btn => {
    btn.addEventListener('click', (e) => {
        const id = btn.getAttribute('data-id');
        const name = btn.getAttribute('data-name');
        const price = parseFloat(btn.getAttribute('data-price'));
        
        addToCart(id, name, price);
        showToast(`Added ${name} to cart`);
        
        // Pop animation on cart badge
        cartBadge.classList.remove('pop');
        void cartBadge.offsetWidth; // trigger reflow
        cartBadge.classList.add('pop');
    });
});

function addToCart(id, name, price) {
    const existingItem = cart.find(item => item.id === id);
    if (existingItem) {
        existingItem.quantity += 1;
    } else {
        cart.push({ id, name, price, quantity: 1 });
    }
    updateCartUI();
}

function removeFromCart(id) {
    cart = cart.filter(item => item.id !== id);
    updateCartUI();
}

function updateQuantity(id, delta) {
    const item = cart.find(item => item.id === id);
    if (item) {
        item.quantity += delta;
        if (item.quantity <= 0) {
            removeFromCart(id);
        } else {
            updateCartUI();
        }
    }
}

function updateCartUI() {
    // Update Badge
    const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
    cartBadge.textContent = totalItems;

    // Update Checkout Button State
    checkoutBtn.disabled = totalItems === 0;

    // Update Items display
    if (cart.length === 0) {
        cartItemsContainer.innerHTML = '<div class="empty-cart-msg">Your cart is currently empty.</div>';
        cartTotalPrice.textContent = '$0.00';
        return;
    }

    cartItemsContainer.innerHTML = '';
    let total = 0;

    cart.forEach(item => {
        total += item.price * item.quantity;
        
        const itemEl = document.createElement('div');
        itemEl.className = 'cart-item';
        itemEl.innerHTML = `
            <div class="cart-item-info">
                <div>
                    <div class="cart-item-title">${item.name}</div>
                    <div class="cart-item-price">$${item.price.toFixed(2)}</div>
                </div>
                <div class="cart-item-actions">
                    <button class="qty-btn" onclick="updateQuantity('${item.id}', -1)">-</button>
                    <span>${item.quantity}</span>
                    <button class="qty-btn" onclick="updateQuantity('${item.id}', 1)">+</button>
                </div>
            </div>
            <div>
                <button class="remove-item" onclick="removeFromCart('${item.id}')">Remove</button>
            </div>
        `;
        cartItemsContainer.appendChild(itemEl);
    });

    cartTotalPrice.textContent = `$${total.toFixed(2)}`;
}

// Make functions global for inline onclick handlers
window.updateQuantity = updateQuantity;
window.removeFromCart = removeFromCart;

// Toast Notification System
function showToast(message) {
    const toast = document.createElement('div');
    toast.className = 'toast show';
    toast.innerHTML = `
        <i data-lucide="check-circle"></i>
        <span>${message}</span>
    `;
    
    toastContainer.appendChild(toast);
    lucide.createIcons({ root: toast });

    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => {
            toast.remove();
        }, 400); // Wait for transition
    }, 3000);
}

// 3D Tilt Effect on Cards (Optional JS enhancement over CSS preserve-3d)
// This makes the card tilt follow the mouse
const cards = document.querySelectorAll('.3d-card');

cards.forEach(card => {
    card.addEventListener('mousemove', (e) => {
        const rect = card.getBoundingClientRect();
        const x = e.clientX - rect.left; // x position within the element.
        const y = e.clientY - rect.top;  // y position within the element.
        
        const centerX = rect.width / 2;
        const centerY = rect.height / 2;
        
        const rotateX = ((y - centerY) / centerY) * -10; // Max 10 deg rotation
        const rotateY = ((x - centerX) / centerX) * 10;
        
        card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale3d(1.05, 1.05, 1.05)`;
    });
    
    card.addEventListener('mouseleave', () => {
        card.style.transform = `perspective(1000px) rotateX(0) rotateY(0) scale3d(1, 1, 1)`;
    });
});
