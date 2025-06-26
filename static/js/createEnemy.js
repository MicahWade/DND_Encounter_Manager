document.querySelector('form').addEventListener('submit', function(e) {
    // You can add additional client-side validation here if needed
    const name = document.getElementById('name').value;
    const hp = document.getElementById('hp').value;
    const CR = document.getElementById('CR').value;
    const STR = document.getElementById('STR').value;
    const DEX = document.getElementById('DEX').value;
    const CON = document.getElementById('CON').value;
    const INT = document.getElementById('INT').value;
    const WIS = document.getElementById('WIS').value;
    const CHA = document.getElementById('CHA').value;
    const size = document.getElementById('size').value;
    const speed = document.getElementById('speed').value;
    const weaponAmount = document.getElementById('weaponAmount').value;
    WeaponNone = false 
    for(let i = 1; i <= weaponAmount; i++){
        weaponName += `+${document.getElementById(`weapon_name_${i}`).value}`;
        weaponDescription += `+${document.getElementById(`weapon_description_${i}`).value}`;
        weaponAttackModifier += `+${document.getElementById(`weapon_attackModifier_${i}`).value}`;
        weaponDamageDice += `+${document.getElementById(`weapon_damageDice_${i}`).value}`;
        WeaponDiceAmount += `+${document.getElementById(`weapon_amount_${i}`).value}`;
        if (!weaponName || !weaponDescription || !weaponAttackModifier || !weaponDamageDice || !WeaponDiceAmount){
            WeaponNone = null
        }
    }
    if (!WeaponNone || !weaponAmount || !name || !hp || !CR || !speed || !weaponName || !weaponDescription || !weaponAttackModifier || !weaponDamageDice || !STR || !DEX || !CON || !INT || !WIS || !CHA || !size) {
        alert('Please fill in all required fields');
        e.preventDefault();
    }
});
function generateWeaponSections() {
    const container = document.getElementById('weaponContainer');
    
    const amount = parseInt(document.getElementById("weaponAmount").value);
    
    // Clear existing sections except the heading
    container.innerHTML = '<h2 class="text-xl font-bold text-gray-900 mb-4">Weapon Details</h2>';
    
    if (isNaN(amount) || amount < 1 || amount > 8) {
        return;
    }
    
    // Initial section template
    for (let i = 1; i <= amount; i++) {
        const initialSection = `
        <select id="Weapon_${i}" 
                name="weapon_${i}" 
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                required>
            <option value="" disabled selected>Select Weapon</option>
            <option value=0>Create Weapon</option>
            <option value=1>defult 1</option>
            <option value=2>defult 2</option>
            <option value=3>defult 3</option>
            <option value=4>defult 4</option>
        </select>
        <div class="border-l-2 border-blue-500 pl-4" id="weapon_list_${i}">
            <label class="block text-gray-700 text-sm font-bold mb-2" for="weapon_name_${i}">
                Weapon ${i} Name
            </label>
            <input type="text" 
                id="weapon_name_${i}"
                name="weapon_name_${i}"
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                required>
            
            <label class="block text-gray-700 text-sm font-bold mb-2" for="weapon_description_${i}">
                Description
            </label>
            <textarea id="weapon_description_${i}" 
                    name="weapon_description_${i}" 
                    class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500" 
                    rows="3"></textarea>
            
            <label class="block text-gray-700 text-sm font-bold mb-2" for="weapon_attackModifier_${i}">
                Attack Modifier
            </label>
            <input type="number" 
                id="weapon_attackModifier_${i}"
                name="weapon_attackModifier_${i}"
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                required>
            
            <label class="block text-gray-700 text-sm font-bold mb-2" for="weapon_damageDice_${i}">
                Damage Dice
            </label>
            <select id="weapon_damageDice_${i}" 
                    name="weapon_damageDice_${i}" 
                    class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    required>
                <option value="" disabled selected>Select Damage Dice</option>
                <option value=4>d4</option>
                <option value=6>d6</option>
                <option value=8>d8</option>
                <option value=10>d10</option>
                <option value=12>d12</option>
            </select>
            
            <label class="block text-gray-700 text-sm font-bold mb-2" for="weapon_amount_${i}">
                Amount Of Dice
            </label>
            <input type="number" 
                id="weapon_amount_${i}"
                name="weapon_amount_${i}"
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                required>
                
            <label class="block text-gray-700 text-sm font-bold mb-2" for="weapon_properties_${i}">
                Properties (comma-separated)
            </label> 
            <input type="text" 
                   id="weapon_properties_${i}" 
                   name="weapon_properties_${i}" 
                   class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500" 
                   required>
            <script>
                const selectWeapon = document.getElementById("weapon_${i}")
                const createWeaponMenu = document.getElementById("weapon_list_${i}")
                
            </script>`;
        let section = initialSection.replace(/\$/g, i);
        const weaponDiv = document.createElement('div');
        weaponDiv.innerHTML = section;
        container.appendChild(weaponDiv);
    }
}

// Generate sections initially
window.onload = generateWeaponSections;
    for (let i = 1; i <= document.getElementById('weaponAmount').value; i++){
        let section = initialSection.replace(/\$/g, i);
        const weaponDiv = document.createElement('div');
        weaponDiv.innerHTML = section;
        container.appendChild(weaponDiv);
    }

// Generate sections initially
window.onload = generateWeaponSections;