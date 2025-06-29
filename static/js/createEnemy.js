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
        weaponName = document.getElementById(`weapon_name_${i}`).value;
        weaponAttackModifier = document.getElementById(`weapon_attackModifier_${i}`).value;
        weaponDamageDice = document.getElementById(`weapon_damageDice_${i}`).value;
        weaponDiceAmount = document.getElementById(`weapon_amount_${i}`).value;
        console.log(!weaponDamageDice)
        console.log(!weaponName)
        console.log(!weaponAttackModifier)
        console.log(!weaponDiceAmount)
        if (!(!weaponName || !weaponAttackModifier || !weaponDamageDice || !weaponDiceAmount)){
            WeaponNone = null
            console.log("weapon")
        }
    }
    if (!(!WeaponNone || !weaponAmount || !name || !hp || !CR || !speed || !STR || !DEX || !CON || !INT || !WIS || !CHA || !size)) {
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
            <label class="block text-gray-700 text-sm font-bold mb-2" for="weapon_type_${i}">
                Weapon Type
            </label>
            <input type="text"
                id="weapon_type_${i}"
                name="weapon_type_${i}"
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                required
                placeholder="e.g. Melee, Ranged">
            <label class="block text-gray-700 text-sm font-bold mb-2" for="weapon_attackModifier_${i}">
                Attack Modifier
            </label>
            <input type="number" 
                id="weapon_attackModifier_${i}"
                name="weapon_attackModifier_${i}"
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                required
                placeholder="+20 | -20">
            <label class="block text-gray-700 text-sm font-bold mb-2" for="weapon_damageType_${i}">
                Damage Type
            </label>
            <select id="weapon_damageType_${i}"
                name="weapon_damageType_${i}"
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                required>
                <option value="" disabled selected>Select Damage Type</option>
                <option value="Bludgeoning">Bludgeoning</option>
                <option value="Piercing">Piercing</option>
                <option value="Slashing">Slashing</option>
                <option value="Acid">Acid</option>
                <option value="Cold">Cold</option>
                <option value="Fire">Fire</option>
                <option value="Force">Force</option>
                <option value="Lightning">Lightning</option>
                <option value="Necrotic">Necrotic</option>
                <option value="Poison">Poison</option>
                <option value="Psychic">Psychic</option>
                <option value="Radiant">Radiant</option>
                <option value="Thunder">Thunder</option>
            </select>
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
    const typeElement = document.getElementById(`weapon_type_${id}`);
    const attackModElement = document.getElementById(`weapon_attackModifier_${id}`);
    const damageTypeElement = document.getElementById(`weapon_damageType_${id}`);
    const damageDiceElement = document.getElementById(`weapon_damageDice_${id}`);
    const diceAmountElement = document.getElementById(`weapon_amount_${id}`);
    const propertiesElement = document.getElementById(`weapon_properties_${id}`);
    const weaponid = document.getElementById(`weapon_${id}`).value;
    if (weaponid != 0 && weaponid !== "" && weaponid !== null) {
        const xhr = new XMLHttpRequest();
        xhr.open("GET", "../weapon/get?weapon=" + encodeURIComponent(weaponid));
        xhr.send();
        xhr.responseType = "json";
        xhr.onload = () => {
            if (xhr.readyState == 4 && xhr.status == 200) {
                const data = xhr.response;
                // Make Elements Read Only 
                nameElement.setAttribute("readOnly", true);
                typeElement.setAttribute("readOnly", true);
                attackModElement.setAttribute("readOnly", true);
                damageTypeElement.setAttribute("disabled", true);
                const damageDiceChildElements = damageDiceElement.children;
                for (let i = 0; i < damageDiceChildElements.length; i++) {
                    if(damageDiceChildElements[i].value != data["dicetype"]){
                        damageDiceChildElements[i].setAttribute("disabled", true);
                    }
                    else{
                        damageDiceChildElements[i].setAttribute("disabled", false);
                        damageDiceChildElements[i].setAttribute("selected", true);
                    }
                };
                diceAmountElement.setAttribute("readOnly", true);
                propertiesElement.setAttribute("readOnly", true);

                nameElement.value = data["name"];
                typeElement.value = data["weaponType"] || "";
                attackModElement.value = data["attackmodifier"];
                damageTypeElement.value = data["damageType"] || "";
                // damageDiceElement.value = data["dicetype"];
                diceAmountElement.value = data["damgedice"];
                propertiesElement.value = data["properties"];
            } else {
                console.log(`Error: ${xhr.status}`);
            }
        } 
    } else {
        nameElement.setAttribute("readOnly", false);
        typeElement.setAttribute("readOnly", false);
        attackModElement.setAttribute("readOnly", false);
        damageTypeElement.removeAttribute("disabled");
        const damageDiceChildElements = damageDiceElement.children;
        for (let i = 0; i < damageDiceChildElements.length; i++) {
            if (damageDiceChildElements[i].value != ""){
                damageDiceChildElements[i].setAttribute("disabled", false);
            } else {
                damageDiceChildElements[i].setAttribute("disabled", true);
                damageDiceChildElements[i].setAttribute("selected", true)
            }
        };
        diceAmountElement.setAttribute("readOnly", false);
        propertiesElement.setAttribute("readOnly", false);
        nameElement.value = "";
        typeElement.value = "";
        attackModElement.value = "";
        damageTypeElement.value = "";
        damageDiceElement.value = "";
        diceAmountElement.value = "";
        propertiesElement.value ="";
    }
}

// Dropdown toggles
function toggleDropdown(id) {
    document.getElementById(id).classList.toggle('hidden');
}

// Languages: collect checked values
function collectLanguages() {
    const checked = Array.from(document.querySelectorAll('input[name="languages_cb"]:checked')).map(cb => cb.value);
    document.getElementById('languages').value = checked.join(', ');
}

// Skills: show input if checked, collect as "Skill +N"
function toggleSkillInput(idx) {
    const cb = document.getElementById('skill_cb_' + idx);
    const input = document.getElementById('skill_val_' + idx);
    input.style.display = cb.checked ? '' : 'none';
}
function collectSkills() {
    const skills = [];
    const skillNames = [
        'Acrobatics', 'Animal Handling', 'Arcana', 'Athletics', 'Deception', 'History', 'Insight', 'Intimidation', 'Investigation', 'Medicine', 'Nature', 'Perception', 'Performance', 'Persuasion', 'Religion', 'Sleight of Hand', 'Stealth', 'Survival'
    ];
    for (let i = 0; i < skillNames.length; i++) {
        const cb = document.getElementById('skill_cb_' + i);
        const val = document.getElementById('skill_val_' + i);
        if (cb && cb.checked && val.value !== "") {
            skills.push(skillNames[i] + " +" + val.value);
        }
    }
    document.getElementById('skills').value = skills.join(', ');
}

// Saving Throws: show input if checked, collect as "STR +N"
function toggleSaveInput(idx) {
    const cb = document.getElementById('save_cb_' + idx);
    const input = document.getElementById('save_val_' + idx);
    input.style.display = cb.checked ? '' : 'none';
}
function collectSaves() {
    const saves = [];
    const saveNames = ['STR', 'DEX', 'CON', 'INT', 'WIS', 'CHA'];
    for (let i = 0; i < saveNames.length; i++) {
        const cb = document.getElementById('save_cb_' + i);
        const val = document.getElementById('save_val_' + i);
        if (cb && cb.checked && val.value !== "") {
            saves.push(saveNames[i] + " +" + val.value);
        }
    }
    document.getElementById('saving_throws').value = saves.join(', ');
}

// Senses: show input if checked, collect as "Sense: value"
function toggleSenseInput(idx) {
    const cb = document.getElementById('sense_cb_' + idx);
    const input = document.getElementById('sense_val_' + idx);
    input.style.display = cb.checked ? '' : 'none';
}
function collectSenses() {
    const senses = [];
    const senseNames = ['Blindsight', 'Darkvision', 'Tremorsense', 'Truesight', 'Passive Perception'];
    for (let i = 0; i < senseNames.length; i++) {
        const cb = document.getElementById('sense_cb_' + i);
        const val = document.getElementById('sense_val_' + i);
        if (cb && cb.checked && val.value !== "") {
            senses.push(senseNames[i] + ": " + val.value);
        }
    }
    document.getElementById('senses').value = senses.join(', ');
}

// Show/hide multiattack field only if more than one weapon and only if it has a value
function showMultiattackField() {
    const amt = parseInt(document.getElementById('weaponAmount').value);
    const field = document.getElementById('multiattackField');
    const input = document.getElementById('multiattack');
    if (amt > 1 && input.value && input.value.trim() !== "") {
        field.style.display = '';
    } else {
        field.style.display = 'none';
    }
}

// Also update on input
document.addEventListener('DOMContentLoaded', function() {
    // Generate weapon sections on load
    generateWeaponSections();
    showMultiattackField();

    // Attach submit handler
    const form = document.getElementById('enemyForm');
    if (form) {
        form.addEventListener('submit', function(e) {
            collectLanguages();
            collectSkills();
            collectSaves();
            collectSenses();
        });
    }

    const multiattackInput = document.getElementById('multiattack');
    if (multiattackInput) {
        multiattackInput.addEventListener('input', showMultiattackField);
    }
});

// Hide dropdowns when clicking outside
document.addEventListener('click', function(e) {
    ['languagesDropdown','skillsDropdown','savingThrowsDropdown','sensesDropdown'].forEach(function(id){
        const btn = e.target.closest('button');
        if (!e.target.closest('#'+id) && (!btn || !btn.onclick || !btn.onclick.toString().includes(id))) {
            const el = document.getElementById(id);
            if (el) el.classList.add('hidden');
        }
    });
});