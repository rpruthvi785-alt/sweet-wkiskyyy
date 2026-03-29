/*=============== SHOW MENU ===============*/
const navMenu = document.getElementById('nav-menu'),
      navToggle = document.getElementById('nav-toggle'),
      navClose = document.getElementById('nav-close')

/*===== MENU SHOW =====*/
if(navToggle){
    navToggle.addEventListener('click', () =>{
        navMenu.classList.add('show-menu')
    })
}

/*===== MENU HIDDEN =====*/
if(navClose){
    navClose.addEventListener('click', () =>{
        navMenu.classList.remove('show-menu')
    })
}

/*=============== REMOVE MENU MOBILE ===============*/
const navLink = document.querySelectorAll('.nav-link')

const linkAction = () =>{
    const navMenu = document.getElementById('nav-menu')
    navMenu.classList.remove('show-menu')
}
navLink.forEach(n => n.addEventListener('click', linkAction))

/*=============== CHANGE BACKGROUND HEADER ===============*/
const scrollHeader = () =>{
    const header = document.getElementById('header')
    if(window.scrollY >= 50) header.classList.add('scroll-header') 
    else header.classList.remove('scroll-header')
}
window.addEventListener('scroll', scrollHeader)

/*=============== SCROLL REVEAL ANIMATION ===============*/
function reveal() {
    var reveals = document.querySelectorAll(".reveal");
    for (var i = 0; i < reveals.length; i++) {
        var windowHeight = window.innerHeight;
        var elementTop = reveals[i].getBoundingClientRect().top;
        var elementVisible = 100;
        if (elementTop < windowHeight - elementVisible) {
            reveals[i].classList.add("active");
        }
    }
}

window.addEventListener("scroll", reveal);
window.addEventListener("load", reveal); 

/*=============== STATE MANAGEMENT ===============*/
const state = {
    cart: JSON.parse(localStorage.getItem('bakery-cart')) || [],
    user: localStorage.getItem('bakery-user') || null,
    products: [],
    filter: 'all',
    checkoutAfterAuth: false
};

/*=============== SUPABASE DB CONFIG ===============*/
const SUPABASE_URL = 'https://ojhenudsmcvuiobpcqsv.supabase.co/rest/v1';
const SUPABASE_KEY = 'sb_publishable_jtGvrWNZ5moIkQj1HwoWQQ_W5nFMfjE';
const HEADERS = {
    'apikey': SUPABASE_KEY,
    'Authorization': `Bearer ${SUPABASE_KEY}`,
    'Content-Type': 'application/json'
};

const db = {
    async signup(username, email, password) {
        try {
            const normalizedUsername = username.toLowerCase().trim();
            const normalizedEmail = email.toLowerCase().trim();

            const res = await fetch(`${SUPABASE_URL}/users`, {
                method: 'POST',
                headers: { ...HEADERS, 'Prefer': 'return=representation' },
                body: JSON.stringify({ 
                    username: normalizedUsername, 
                    email: normalizedEmail, 
                    password 
                })
            });

            if (res.ok) return { success: true, user: normalizedUsername };
            
            const err = await res.json();
            if (err.code === '23505') {
                if (err.message.includes('username')) return { success: false, message: 'Username already exists' };
                if (err.message.includes('email')) return { success: false, message: 'Email already registered' };
            }
            return { success: false, message: err.message || 'Error creating account' };
        } catch (e) {
            return { success: false, message: 'Network error. Please try again.' };
        }
    },

    async login(username, password) {
        try {
            const normalizedUsername = username.toLowerCase().trim();
            const res = await fetch(`${SUPABASE_URL}/users?username=eq.${normalizedUsername}&password=eq.${password}`, { headers: HEADERS });
            if (!res.ok) throw new Error('Query failed');
            
            const users = await res.json();
            if (users.length > 0) return { success: true, user: users[0].username };
            return { success: false, message: 'Invalid username or password' };
        } catch (e) {
            return { success: false, message: 'Unable to connect to login server.' };
        }
    },

    async checkout(username, cart, orderType) {
        try {
            if (!cart || cart.length === 0) return { success: false, message: 'Cart is empty' };
            
            const now = new Date().toISOString();
            const orders = cart.map(item => ({
                username: username.toLowerCase().trim(),
                product_name: item.name,
                price: parseFloat(item.price),
                quantity: parseInt(item.quantity),
                order_type: orderType,
                status: 'baking',
                ordered_at: now,
                custom_details: item.details || ''
            }));

            const res = await fetch(`${SUPABASE_URL}/orders`, {
                method: 'POST',
                headers: { ...HEADERS, 'Prefer': 'return=minimal' },
                body: JSON.stringify(orders)
            });

            if (res.ok) return { success: true };
            const err = await res.json();
            return { success: false, message: err.message || 'Payment processing failed' };
        } catch (e) {
            return { success: false, message: 'Network error during checkout.' };
        }
    },

    async history(username) {
        try {
            const normalizedUsername = username.toLowerCase().trim();
            const res = await fetch(`${SUPABASE_URL}/orders?username=eq.${normalizedUsername}&order=ordered_at.desc`, { headers: HEADERS });
            if (res.ok) return await res.json();
            return [];
        } catch (e) {
            return [];
        }
    }
};

/*=============== ELEMENTS ===============*/
const menuGrid = document.querySelector('.menu-grid');
const filterBtns = document.querySelectorAll('.filter-btn');
const btnLogin = document.getElementById('btn-login');
const btnLogout = document.getElementById('btn-logout');
const btnCart = document.getElementById('btn-cart');
const loginModal = document.getElementById('login-modal');
const signupModal = document.getElementById('signup-modal');
const cartModal = document.getElementById('cart-modal');
const confirmModal = document.getElementById('confirm-modal');
const closeLogin = document.getElementById('close-login');
const closeSignup = document.getElementById('close-signup');
const closeCart = document.getElementById('close-cart');
const closeConfirm = document.getElementById('close-confirm');
const loginForm = document.getElementById('login-form');
const signupForm = document.getElementById('signup-form');
const cartItemsContainer = document.getElementById('cart-items');
const cartTotalPrice = document.getElementById('cart-total-price');
const cartCount = document.getElementById('cart-count');
const btnCheckout = document.getElementById('btn-checkout');
const btnContinue = document.getElementById('btn-continue');
const loginError = document.getElementById('login-error');
const signupError = document.getElementById('signup-error');
const linkSignup = document.getElementById('link-signup');
const linkLogin = document.getElementById('link-login');

const btnHistory = document.getElementById('btn-history');
const historyModal = document.getElementById('history-modal');
const historyItemsContainer = document.getElementById('history-items');
const closeHistory = document.getElementById('close-history');
const btnCloseHistoryUI = document.getElementById('btn-close-history-ui');
const btnMakeOwn = document.getElementById('btn-make-own');
const customModal = document.getElementById('custom-modal');
const closeCustom = document.getElementById('close-custom');
const customCakeForm = document.getElementById('custom-cake-form');
const customPriceDisplay = document.getElementById('custom-price-display');

/*=============== MODAL HELPERS ===============*/
const openModal = (modal) => modal.classList.add('show-modal');
const closeModal = (modal) => modal.classList.remove('show-modal');

/*=============== UI UPDATES ===============*/
async function updateAuthUI() {
    if (state.user) {
        btnLogin.textContent = `Hi, ${state.user}`;
        btnLogin.style.pointerEvents = 'none';
        btnLogout.style.display = 'block';
        btnHistory.style.display = 'block';
        document.getElementById('tracking-login-prompt').style.display = 'none';
        document.getElementById('tracking-display').style.display = 'block';
        await updateTrackingUI();
    } else {
        btnLogin.textContent = "Sign In";
        btnLogin.style.pointerEvents = 'auto';
        btnLogout.style.display = 'none';
        btnHistory.style.display = 'none';
        document.getElementById('tracking-login-prompt').style.display = 'block';
        document.getElementById('tracking-display').style.display = 'none';
    }
}

async function updateHistoryUI() {
    if (!state.user) return;
    historyItemsContainer.innerHTML = '<p style="text-align: center; padding: 1rem;">Loading...</p>';
    const history = await db.history(state.user);
    if (history.length === 0) {
        historyItemsContainer.innerHTML = '<p style="color: gray; text-align: center; padding: 1rem;">No history found. Time to buy some cake!</p>';
    } else {
        historyItemsContainer.innerHTML = history.map(item => `
            <div class="history-item" style="padding: 1rem; border-bottom: 1px solid #eee;">
                <div style="display: flex; justify-content: space-between;">
                    <strong style="color: var(--primary-color);">${item.product_name}</strong>
                    <span>$${(item.price * item.quantity).toFixed(2)}</span>
                </div>
                <div style="font-size: 0.85rem; color: gray; margin-top: 0.25rem;">
                    Qty: ${item.quantity} | ${new Date(item.ordered_at).toLocaleDateString()}
                </div>
            </div>
        `).join('');
    }
}

async function updateTrackingUI() {
    if (!state.user) return;
    const history = await db.history(state.user);
    const trackingDisplay = document.getElementById('tracking-display');

    if (history.length === 0) {
        trackingDisplay.innerHTML = '<p style="color: gray; text-align: center;">No active orders to track. Go get some cake!</p>';
        return;
    }

    const now = new Date();
    const activeOrders = history.filter(order => {
        const orderTime = new Date(order.ordered_at);
        return (now - orderTime) < (2 * 60 * 60 * 1000);
    });

    if (activeOrders.length === 0) {
        trackingDisplay.innerHTML = '<p style="color: gray; text-align: center;">Current orders are complete. View History for older bakes.</p>';
        return;
    }

    trackingDisplay.innerHTML = activeOrders.map(order => {
        const orderTime = new Date(order.ordered_at);
        const secondsElapsed = (now - orderTime) / 1000;
        const displayStatus = secondsElapsed > 30 ? 'delivered' : order.status;

        return `
        <div class="tracking-item" style="margin-bottom: 2rem; border-bottom: 1px solid #eee; padding-bottom: 1.5rem;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 1rem;">
                <h4 style="color: var(--sec-color); margin:0;">${order.product_name}</h4>
                <span class="badge" style="background: var(--primary-color); color: #fff; padding: 0.2rem 0.6rem; border-radius: 4px; font-size: 0.8rem; text-transform: uppercase;">${order.order_type}</span>
            </div>
            <div class="status-stepper" style="display: flex; justify-content: space-between; position: relative; margin-top: 1rem;">
                <div style="text-align: center; flex: 1;">
                    <div style="width: 20px; height: 20px; background: var(--primary-color); border-radius: 50%; margin: 0 auto;"></div>
                    <p style="font-size: 0.7rem; margin-top: 0.5rem; color: var(--primary-color); font-weight: bold;">Baking</p>
                </div>
                <div style="text-align: center; flex: 1;">
                    <div style="width: 20px; height: 20px; background: ${displayStatus === 'delivered' ? 'var(--primary-color)' : '#ccc'}; border-radius: 50%; margin: 0 auto; transition: background 0.5s ease;"></div>
                    <p style="font-size: 0.7rem; margin-top: 0.5rem; color: ${displayStatus === 'delivered' ? 'var(--primary-color)' : '#999'}; ${displayStatus === 'delivered' ? 'font-weight: bold;' : ''}">
                        ${order.order_type === 'delivery' ? 'Out for Delivery' : 'Ready to Serve'}
                    </p>
                </div>
            </div>
            ${displayStatus === 'baking' ? `<p style="font-size: 0.75rem; color: #666; text-align: center; margin-top: 1rem;">Estimated time: ${Math.max(0, Math.floor(30 - secondsElapsed))}s remaining...</p>` : ''}
        </div>
        `;
    }).join('');
}

function updateCartUI() {
    localStorage.setItem('bakery-cart', JSON.stringify(state.cart));
    cartCount.textContent = state.cart.reduce((sum, item) => sum + item.quantity, 0);
    let total = 0;
    
    if (state.cart.length === 0) {
        cartItemsContainer.innerHTML = '<p style="color: gray; text-align: center; margin-top: 1rem;">Your cart is empty.</p>';
    } else {
        cartItemsContainer.innerHTML = '';
        state.cart.forEach((item, index) => {
            total += item.price * item.quantity;
            
            const cartItemHTML = `
                <div class="cart-item" style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #eee; padding-bottom: 0.75rem; margin-bottom: 0.75rem;">
                    <div style="flex: 1;">
                        <span style="font-weight: 600;">${item.name}</span><br>
                        ${item.details ? `<span style="font-size: 0.75rem; color: #666; display: block; margin-bottom: 0.25rem;">${item.details}</span>` : ''}
                        <span style="color: var(--text-color-light); font-size: 0.9rem;">$${item.price.toFixed(2)} each</span>
                    </div>
                    <div style="display: flex; align-items: center; gap: 0.5rem;">
                        <button type="button" class="btn-qty-decrease" data-index="${index}" style="width: 28px; height: 28px; border-radius: 4px; border: 1px solid #ccc; background: #fff; cursor: pointer;">-</button>
                        <span style="width: 20px; text-align: center;">${item.quantity}</span>
                        <button type="button" class="btn-qty-increase" data-index="${index}" style="width: 28px; height: 28px; border-radius: 4px; border: 1px solid #ccc; background: #fff; cursor: pointer;">+</button>
                        <button type="button" class="btn-remove-item" data-index="${index}" style="width: 30px; height: 30px; margin-left: 0.5rem; border-radius: 4px; border: none; background: #ffe4e4; color: #dc2626; cursor: pointer;" title="Remove Item">
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="pointer-events: none;"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path></svg>
                        </button>
                    </div>
                </div>
            `;
            cartItemsContainer.insertAdjacentHTML('beforeend', cartItemHTML);
        });

        document.querySelectorAll('.btn-qty-decrease').forEach(btn => {
            btn.onclick = (e) => {
                const idx = parseInt(e.target.getAttribute('data-index'));
                if (state.cart[idx].quantity > 1) state.cart[idx].quantity -= 1;
                else state.cart.splice(idx, 1);
                updateCartUI();
            };
        });

        document.querySelectorAll('.btn-qty-increase').forEach(btn => {
            btn.onclick = (e) => {
                const idx = parseInt(e.target.getAttribute('data-index'));
                state.cart[idx].quantity += 1;
                updateCartUI();
            };
        });

        document.querySelectorAll('.btn-remove-item').forEach(btn => {
            btn.onclick = (e) => {
                const idx = parseInt(btn.getAttribute('data-index'));
                state.cart.splice(idx, 1);
                updateCartUI();
            };
        });
    }
    cartTotalPrice.textContent = total.toFixed(2);
}

/*=============== PRODUCT RENDERING ===============*/
function renderProducts() {
    const filtered = state.products.filter(p => state.filter === 'all' || p.category === state.filter);
    
    if (filtered.length === 0) {
        menuGrid.innerHTML = '<p style="text-align:center; color:gray; padding:2rem; width:100%;">No products found in the database.</p>';
        return;
    }

    menuGrid.innerHTML = filtered.map((product, index) => `
        <article class="menu-item reveal" data-category="${product.category}" style="display: block;">
            <div class="menu-img-wrapper" style="background-color: #f3f3f3;">
                <img src="${product.image_path}" alt="${product.name}" class="menu-img" onerror="this.onerror=null;this.src='https://images.pexels.com/photos/1721932/pexels-photo-1721932.jpeg?auto=compress&cs=tinysrgb&w=600';">
                ${product.is_bestseller ? '<div class="menu-badge">Bestseller</div>' : ''}
            </div>
            <div class="menu-content">
                <h3 class="menu-title">${product.name}</h3>
                <p class="menu-desc">${product.description}</p>
                <div class="menu-footer">
                    <span class="menu-price">$${Number(product.price).toFixed(2)}</span>
                    <button type="button" class="btn btn-sm btn-primary add-to-cart-btn" 
                        data-name="${product.name}" data-price="${product.price}">Add to Cart</button>
                </div>
            </div>
        </article>
    `).join('');

    document.querySelectorAll('.add-to-cart-btn').forEach(btn => {
        btn.onclick = () => {
            const name = btn.getAttribute('data-name');
            const price = parseFloat(btn.getAttribute('data-price'));
            
            const existingItem = state.cart.find(item => item.name === name);
            if (existingItem) existingItem.quantity += 1;
            else state.cart.push({ name, price, quantity: 1 });
            
            updateCartUI();
            alert(`${name} added to cart!`);
        };
    });

    reveal();
}

/*=============== DATA FETCHING ===============*/
async function fetchProducts() {
    try {
        // Retrieve products directly from Supabase!
        const response = await fetch(`${SUPABASE_URL}/products?order=id.asc`, { headers: HEADERS });
        if (response.ok) {
            state.products = await response.json();
            renderProducts();
            reveal();
            setTimeout(reveal, 200);
        } else {
            throw new Error(`Supabase returned ${response.status}`);
        }
    } catch (err) {
        console.error("Failed to fetch products:", err);
        // Fallback to local JSON if supabase fails/has no tables
        try {
            const fallbackRes = await fetch('products.json');
            state.products = await fallbackRes.json();
            renderProducts();
        } catch (e) {
            if (menuGrid) menuGrid.innerHTML = '<p style="text-align:center; color:gray; padding:2rem; width:100%;">Unable to load products. Have you connected to Supabase yet?</p>';
        }
    }
}

/*=============== EVENT LISTENERS ===============*/
filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        filterBtns.forEach(b => {
            b.classList.remove('btn-primary', 'active');
            b.classList.add('btn-outline');
        });
        btn.classList.remove('btn-outline');
        btn.classList.add('btn-primary', 'active');
        
        state.filter = btn.getAttribute('data-filter');
        renderProducts();
    });
});

btnLogin.addEventListener('click', () => { if (!state.user) openModal(loginModal); });
btnLogout.addEventListener('click', () => {
    state.user = null;
    localStorage.removeItem('bakery-user');
    updateAuthUI();
});
btnCart.addEventListener('click', () => openModal(cartModal));
btnHistory.addEventListener('click', async () => {
    openModal(historyModal);
    await updateHistoryUI();
});

closeLogin.addEventListener('click', () => closeModal(loginModal));
closeSignup.addEventListener('click', () => closeModal(signupModal));
closeCart.addEventListener('click', () => closeModal(cartModal));
closeHistory.addEventListener('click', () => closeModal(historyModal));
btnCloseHistoryUI.addEventListener('click', () => closeModal(historyModal));
if (closeCustom) closeCustom.addEventListener('click', () => closeModal(customModal));
if (btnMakeOwn) btnMakeOwn.addEventListener('click', () => openModal(customModal));

if (customCakeForm) {
    const updateCustomPrice = () => {
        const flavorPrice = parseFloat(document.getElementById('custom-flavor').selectedOptions[0].getAttribute('data-price'));
        const sizeMultiplier = parseFloat(document.getElementById('custom-size').selectedOptions[0].getAttribute('data-multiplier'));
        let extras = 0;
        document.querySelectorAll('input[name="topping"]:checked').forEach(cb => {
            extras += parseFloat(cb.getAttribute('data-price'));
        });
        const frostingPrice = parseFloat(document.querySelector('input[name="frosting"]:checked').getAttribute('data-price'));
        extras += frostingPrice;
        const totalPrice = (flavorPrice * sizeMultiplier) + extras;
        customPriceDisplay.textContent = totalPrice.toFixed(2);
        return totalPrice;
    };

    customCakeForm.addEventListener('change', updateCustomPrice);
    btnMakeOwn.addEventListener('click', updateCustomPrice);

    customCakeForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const flavor = document.getElementById('custom-flavor').value;
        const size = document.getElementById('custom-size').value;
        const frosting = document.querySelector('input[name="frosting"]:checked').value;
        const toppings = Array.from(document.querySelectorAll('input[name="topping"]:checked')).map(cb => cb.value);
        const message = document.getElementById('custom-message').value;
        const price = updateCustomPrice();

        const details = `Flavor: ${flavor}, Size: ${size}, Frosting: ${frosting}${toppings.length ? `, Toppings: ${toppings.join(', ')}` : ''}${message ? `, Msg: "${message}"` : ''}`;
        
        state.cart.push({
            name: "Custom Cake",
            price: price,
            quantity: 1,
            details: details
        });

        updateCartUI();
        closeModal(customModal);
        customCakeForm.reset();
        alert("Custom cake added to cart!");
    });
}
if(closeConfirm) closeConfirm.addEventListener('click', () => closeModal(confirmModal));
if(btnContinue) btnContinue.addEventListener('click', () => closeModal(confirmModal));

linkSignup.addEventListener('click', (e) => { e.preventDefault(); closeModal(loginModal); openModal(signupModal); });
linkLogin.addEventListener('click', (e) => { e.preventDefault(); closeModal(signupModal); openModal(loginModal); });

window.addEventListener('click', (e) => {
    if (e.target === loginModal) closeModal(loginModal);
    if (e.target === signupModal) closeModal(signupModal);
    if (e.target === cartModal) closeModal(cartModal);
    if (e.target === historyModal) closeModal(historyModal);
    if (e.target === confirmModal) closeModal(confirmModal);
    if (e.target === customModal) closeModal(customModal);
});

loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const btnSubmit = loginForm.querySelector('button[type="submit"]');
    btnSubmit.textContent = "Loading...";
    btnSubmit.disabled = true;
    
    const username = document.getElementById('login-username').value.trim();
    const password = document.getElementById('login-password').value;
    loginError.style.display = 'none';

    const result = await db.login(username, password);
    
    btnSubmit.textContent = "Sign In";
    btnSubmit.disabled = false;

    if (result.success) {
        state.user = result.user;
        localStorage.setItem('bakery-user', state.user);
        updateAuthUI();
        closeModal(loginModal);
        loginForm.reset();
        
        // Auto-resume checkout if pending
        if (state.checkoutAfterAuth) {
            state.checkoutAfterAuth = false;
            openModal(cartModal);
            setTimeout(() => {
                const checkoutBtn = document.getElementById('btn-checkout');
                if (checkoutBtn) checkoutBtn.click();
            }, 500);
        }
    } else {
        loginError.textContent = result.message;
        loginError.style.display = 'block';
    }
});

signupForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const btnSubmit = signupForm.querySelector('button[type="submit"]');
    btnSubmit.textContent = "Loading...";
    btnSubmit.disabled = true;

    const username = document.getElementById('signup-username').value.trim();
    const email = document.getElementById('signup-email').value.trim();
    const password = document.getElementById('signup-password').value;
    signupError.style.display = 'none';

    if (!username || !email || !password) {
        signupError.textContent = 'All fields are required.';
        signupError.style.display = 'block';
        btnSubmit.textContent = "Create Account";
        btnSubmit.disabled = false;
        return;
    }

    const result = await db.signup(username, email, password);
    
    btnSubmit.textContent = "Create Account";
    btnSubmit.disabled = false;

    if (result.success) {
        state.user = result.user;
        localStorage.setItem('bakery-user', state.user);
        updateAuthUI();
        closeModal(signupModal);
        signupForm.reset();
        alert('Account created successfully!');

        // Auto-resume checkout if pending
        if (state.checkoutAfterAuth) {
            state.checkoutAfterAuth = false;
            openModal(cartModal);
            setTimeout(() => {
                const checkoutBtn = document.getElementById('btn-checkout');
                if (checkoutBtn) checkoutBtn.click();
            }, 500);
        }
    } else {
        signupError.textContent = result.message;
        signupError.style.display = 'block';
    }
});

btnCheckout.addEventListener('click', async () => {
    if (state.cart.length === 0) return alert('Your cart is empty.');
    if (!state.user) {
        state.checkoutAfterAuth = true;
        closeModal(cartModal);
        openModal(loginModal);
        alert('Please sign in to complete your purchase.');
        return;
    }

    btnCheckout.textContent = "Processing...";
    btnCheckout.disabled = true;

    const orderType = document.querySelector('input[name="order-type"]:checked').value;
    const result = await db.checkout(state.user, state.cart, orderType);

    btnCheckout.textContent = "Checkout Now";
    btnCheckout.disabled = false;

    if (result.success) {
        state.cart = [];
        updateCartUI();
        await updateTrackingUI();
        closeModal(cartModal);
        openModal(confirmModal);

        let ticks = 0;
        const liveRefresh = setInterval(async () => {
            await updateTrackingUI();
            ticks++;
            if (ticks > 35) clearInterval(liveRefresh);
        }, 1000);
    } else {
        alert('Checkout failed: ' + (result.message || 'Please try again.'));
    }
});

/*=============== INITIALIZATION ===============*/
window.addEventListener('DOMContentLoaded', () => {
    updateAuthUI();
    updateCartUI();
    fetchProducts();
});
