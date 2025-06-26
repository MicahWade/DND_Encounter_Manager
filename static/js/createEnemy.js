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
        <select id="weapon_${i}" 
                name="weapon_${i}" 
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                required
                oninput="sendWeaponRequest('${i}')">
            <option value="" disabled selected>Select Weapon</option>
            <option value=0>Create Weapon</option>
            <optgroup label="Simple Melee Weapons">
                <option value=6>Club</option>
                <option value=4>Dagger</option>
                <option value=14>Mace</option>
                <option value=16>Quarterstaff</option>
                <option value=22>Sickle</option>
                <option value=17>Spear</option>
                <option value=8>Handaxe</option>
            </optgroup>
            <optgroup label="Simple Ranged Weapons">
                <option value=5>Light Crossbow</option>
                <option value=26>Sling</option>
                <option value=27>Shortbow</option>
                <option value=31>Dart</option>
                <option value=32>Javelin</option>
            </optgroup>
            <optgroup label="Martial Melee Weapons">
                <option value=1>Longsword</option>
                <option value=2>Greatsword</option>
                <option value=7>Battleaxe</option>
                <option value=9>Greataxe</option>
                <option value=10>Halberd</option>
                <option value=11>Glaive</option>
                <option value=12>Maul</option>
                <option value=13>Warhammer</option>
                <option value=15>Morningstar</option>
                <option value=18>Rapier</option>
                <option value=19>Scimitar</option>
                <option value=20>Trident</option>
                <option value=21>Whip</option>
                <option value=23>Flail</option>
                <option value=24>Pike</option>
                <option value=25>Lance</option>
            </optgroup>
            <optgroup label="Martial Ranged Weapons">
                <option value=28>Longbow</option>
                <option value=29>Heavy Crossbow</option>
                <option value=30>Blowgun</option>
                <option value=33>Net</option>
            </optgroup>
        </select>
        <div class="border-l-2 border-blue-500 pl-4" id="weapon_list_${i}">
            <label class="block text-gray-700 text-sm font-bold mb-2" for="weapon_name_${i}">
                Weapon ${i} Name
            </label>
            <input type="text" 
                id="weapon_name_${i}"
                name="weapon_name_${i}"
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                required
                placeholder="name....">
            <label class="block text-gray-700 text-sm font-bold mb-2" for="weapon_attackModifier_${i}">
                Attack Modifier
            </label>
            <input type="number" 
                id="weapon_attackModifier_${i}"
                name="weapon_attackModifier_${i}"
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                required
                placeholder="+20 | -20">
            
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
                required
                placeholder="1...">
                
            <label class="block text-gray-700 text-sm font-bold mb-2" for="weapon_properties_${i}">
                Properties (comma-separated)
            </label> 
            <input type="text" 
                   id="weapon_properties_${i}" 
                   name="weapon_properties_${i}" 
                   class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500" 
                   required
                   placeholder="Heavy, two-handed">`;
        let section = initialSection.replace(/\$/g, i);
        const weaponDiv = document.createElement('div');
        weaponDiv.innerHTML = section;
        container.appendChild(weaponDiv);
    }
}

function sendWeaponRequest(id){
    // Get Elements
    const nameElement = document.getElementById(`weapon_name_${id}`);
    const attackModElement = document.getElementById(`weapon_attackModifier_${id}`);
    const damageDiceElement = document.getElementById(`weapon_damageDice_${id}`);
    const diceAmountElement = document.getElementById(`weapon_amount_${id}`);
    const propertiesElement = document.getElementById(`weapon_properties_${id}`);
    const weaponid = document.getElementById(`weapon_${id}`).value;
    if (weaponid != 0){
        const xhr = new XMLHttpRequest();
        xhr.open("GET", "../weapon/get?weapon=" + encodeURIComponent(weaponid));
        xhr.send();
        xhr.responseType = "json";
        xhr.onload = () => {
        if (xhr.readyState == 4 && xhr.status == 200) {
            const data = xhr.response;
            // Make Elements Read Only 
            nameElement.setAttribute("readOnly", true);
            attackModElement.setAttribute("readOnly", true);
            const damageDiceChildElements = damageDiceElement.children;
            for (let i = 0; i < damageDiceChildElements.length; i++) {
                if(damageDiceChildElements[i].value != data["dicetype"]){
                    damageDiceChildElements[i].setAttribute("disabled", true);
                }
            };
            diceAmountElement.setAttribute("readOnly", true);
            propertiesElement.setAttribute("readOnly", true);

            nameElement.value = data["name"];
            attackModElement.value = data["attackmodifier"];
            damageDiceElement.value = data["dicetype"];
            diceAmountElement.value = data["damgedice"];
            propertiesElement.value = data["properties"];
        } else {
            console.log(`Error: ${xhr.status}`);
        }
    } 
    } else {
        nameElement.setAttribute("readOnly", false);
        attackModElement.setAttribute("readOnly", false);
        const damageDiceChildElements = damageDiceElement.children;
        for (let i = 0; i < damageDiceChildElements.length; i++) {
            if (damageDiceChildElements[i].value != ""){
                damageDiceChildElements[i].setAttribute("disabled", false);
            }
        };
        diceAmountElement.setAttribute("readOnly", false);
        propertiesElement.setAttribute("readOnly", false);
        nameElement.value = "";
        attackModElement.value = "";
        damageDiceElement.value = "";
        diceAmountElement.value = "";
        propertiesElement.value ="";
    }
}

// Generate sections initially
window.onload = generateWeaponSections();