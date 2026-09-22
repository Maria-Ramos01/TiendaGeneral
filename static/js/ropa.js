// Lógica interactiva específica para la tienda de ropa
document.addEventListener('DOMContentLoaded', () => {
console.log('Módulo de tienda de ropa cargado.');
initRopaOptions();
});

function initRopaOptions() {
const container = document.getElementById('tienda-custom-options');
if (!container) return;

container.innerHTML = `
    <div class="option-group size-selector" style="margin: 1rem 0;">
        <label><strong>Selecciona tu talla:</strong></label><br>
        <button type="button" onclick="selectSize(this)">S</button>
        <button type="button" onclick="selectSize(this)">M</button>
        <button type="button" onclick="selectSize(this)">L</button>
        <button type="button" onclick="selectSize(this)">XL</button>
    </div>
`;


}

function selectSize(btn) {
const buttons = btn.parentElement.querySelectorAll('button');
buttons.forEach(b => b.classList.remove('selected'));
btn.classList.add('selected');
}