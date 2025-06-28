const burger = document.querySelector('.burger');
const mobileMenu = document.querySelector('.mobile-menu');
const openSearch = document.getElementById('openSearch');
const openSearchMobile = document.getElementById('openSearchMobile');
const modal = document.getElementById('searchModal');
const close = document.querySelector('.close');

burger.addEventListener('click', () => {
mobileMenu.classList.toggle('active');
});

        // Open search modal
openSearch.addEventListener('click', (e) => {
e.preventDefault();
modal.style.display = 'block';
});

openSearchMobile.addEventListener('click', (e) => {
e.preventDefault();
modal.style.display = 'block';
});

close.addEventListener('click', () => {
modal.style.display = 'none';
});

window.addEventListener('click', (e) => {
if (e.target === modal) {
modal.style.display = 'none';
}
});

let cartItems = JSON.parse(localStorage.getItem('cartItems')) || [];
const cartCounter = document.getElementById('cart-counter');
const cartCounterMobile = document.getElementById('cart-counter-mobile');

function updateCartCounter() {
const itemCount = cartItems.reduce((total, item) => total + item.quantity, 0);
cartCounter.textContent = itemCount;
cartCounterMobile.textContent = itemCount;
}

updateCartCounter();