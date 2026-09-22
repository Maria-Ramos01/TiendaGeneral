// Lógica interactiva específica para la tienda de lanas
document.addEventListener('DOMContentLoaded', () => {
console.log('Módulo de tienda de lanas cargado.');
initLanasCalculator();
});

function initLanasCalculator() {
const container = document.getElementById('tienda-custom-options');
if (!container) return;

container.innerHTML = `
    <div class="lanas-calc" style="background: #f0e6df; padding: 10px; border-radius: 8px; margin: 1rem 0;">
        <h4>Calculadora de Ovillos Estimada</h4>
        <p style="font-size: 0.85rem;">¿Qué vas a tejer?</p>
        <select id="proyecto-select" onchange="calculateYarn()" style="padding: 5px; margin-top: 5px;">
            <option value="1">Bufanda (Aprox. 2 ovillos)</option>
            <option value="4">Gorro (Aprox. 1 ovillo)</option>
            <option value="6">Suéter (Aprox. 6 ovillos)</option>
        </select>
        <p id="yarn-result" style="margin-top: 5px; font-weight: bold; color: #8b5a2b;"></p>
    </div>
`;


}

function calculateYarn() {
const val = document.getElementById('proyecto-select').value;
document.getElementById('yarn-result').innerText = `Recomendación: Compra al menos ${val} unidad(es).`;}
