const encounterElementsBox = document.getElementById('encounterElementsBox');
const encounterElementsList = document.getElementById('encounterElementsList');
const encounterElementsPlaceholder = document.getElementById('encounterElementsPlaceholder');
const addTypeListItem = document.getElementById('addTypeListItem');
const addTypeBtn = document.getElementById('addTypeBtn');
const addTypeDropdown = document.getElementById('addTypeDropdown');


function addDescription(li) {
    // Main row (flex for parent)
    const row = document.createElement('div');
    row.className = "flex items-center justify-between w-full";

    const span = document.createElement('span');
    span.textContent = "Description";

    const removeBtn = document.createElement('button');
    removeBtn.className = "text-red-500 hover:text-red-700 ml-2";
    removeBtn.title = "Remove";
    removeBtn.type = "button";
    removeBtn.innerHTML = "&times;";
    removeBtn.addEventListener('click', () => {
        li.remove();
        if (encounterElementsList.querySelectorAll('li:not(#addTypeListItem)').length === 0 && encounterElementsPlaceholder) {
            encounterElementsPlaceholder.style.display = '';
        }
    });

    row.appendChild(span);
    row.appendChild(removeBtn);
    li.appendChild(row);

    const descriptionContainer = document.createElement('div');
    descriptionContainer.className = 'ml-4 mt-2 p-2 border-l-2 border-slate-300';

    const textarea = document.createElement('textarea');
    textarea.className = 'w-full p-2 border border-slate-400 rounded-md text-sm';
    textarea.rows = 4;
    textarea.placeholder = 'Enter description here...';

    descriptionContainer.appendChild(textarea);
    li.appendChild(descriptionContainer);
}

function addBattle(subLi) {
    const row = document.createElement('div');
    row.className = "flex items-center justify-between";
    // Label
    const span = document.createElement('span');
    span.textContent = "Battle";
    // Remove button
    const removeBtn = document.createElement('button');
    removeBtn.className = "text-red-500 hover:text-red-700 ml-2";
    removeBtn.title = "Remove";
    removeBtn.type = "button";
    removeBtn.innerHTML = "&times;";
    removeBtn.addEventListener('click', () => {
        subLi.remove();
    });
    // Assemble row
    row.appendChild(span);
    row.appendChild(removeBtn);
    subLi.appendChild(row);
    // If this type can have children, add a nested UL and Add Encounter button
    const subList = document.createElement('ul');
    subList.className = "ml-8 mt-2 space-y-2";
    // Add Encounter button (as a list item)
    const addBtnLi = document.createElement('li');
    const typeSelector = createAddElementSelector();
    addBtnLi.appendChild(typeSelector);
    subList.appendChild(addBtnLi); // Always keep this as the last <li>
    subLi.appendChild(subList);
}

function addSkillCheck(li) {
    li.className = "bg-slate-200/30 border border-slate-300 rounded px-3 py-2 mb-2";

    // Main row (flex for parent)
    const row = document.createElement('div');
    row.className = "flex items-center justify-between";

    const span = document.createElement('span');
    span.textContent = "Skill Check";

    const removeBtn = document.createElement('button');
    removeBtn.className = "text-red-500 hover:text-red-700 ml-2";
    removeBtn.title = "Remove";
    removeBtn.type = "button";
    removeBtn.innerHTML = "&times;";
    removeBtn.addEventListener('click', () => {
        li.remove();
        if (encounterElementsList.querySelectorAll('li:not(#addTypeListItem)').length === 0 && encounterElementsPlaceholder) {
            encounterElementsPlaceholder.style.display = '';
        }
    });

    row.appendChild(span);
    row.appendChild(removeBtn);
    li.appendChild(row);

    const skillCheckContainer = document.createElement('div');
    skillCheckContainer.className = 'ml-4 mt-2 p-2 border-l-2 border-slate-300';

    // Inputs for Skill and DC
    const inputsDiv = document.createElement('div');
    inputsDiv.className = 'flex items-center gap-4 mb-2';
    inputsDiv.innerHTML = `
        <label for="skill-name" class="text-sm font-medium">Skill:</label>                    
        <select name="skill-name-select" class="p-1 border border-slate-400 rounded-md text-sm w-48">
            <option value="">Select Skill</option>
            <option value="Acrobatics">Acrobatics (Dex)</option>
            <option value="Animal Handling">Animal Handling (Wis)</option>
            <option value="Arcana">Arcana (Int)</option>
            <option value="Athletics">Athletics (Str)</option>
            <option value="Deception">Deception (Cha)</option>
            <option value="History">History (Int)</option>
            <option value="Insight">Insight (Wis)</option>
            <option value="Intimidation">Intimidation (Cha)</option>
            <option value="Investigation">Investigation (Int)</option>
            <option value="Medicine">Medicine (Wis)</option>
            <option value="Nature">Nature (Int)</option>
            <option value="Perception">Perception (Wis)</option>
            <option value="Performance">Performance (Cha)</option>
            <option value="Persuasion">Persuasion (Cha)</option>
            <option value="Religion">Religion (Int)</option>
            <option value="Sleight of Hand">Sleight of Hand (Dex)</option>
            <option value="Stealth">Stealth (Dex)</option>
            <option value="Survival">Survival (Wis)</option>
        </sele
        <label for="skill-dc" class="text-sm font-medium">DC:</label>
        <input type="number" name="skill-dc" class="p-1 border border-slate-400 rounded-md w-16 text-sm" placeholder="15">
    `;
    skillCheckContainer.appendChild(inputsDiv);
    // Success branch
    const successDiv = document.createElement('div');
    successDiv.className = 'mt-2 w-full';
    const successHeader = document.createElement('h4');
    successHeader.className = 'font-semibold text-green-700';
    successHeader.textContent = 'On Success';
    const successList = document.createElement('ul');
    successList.className = "ml-2 mt-2 space-y-2 w-full";
    const addSuccessBtnLi = document.createElement('li');
    const addSuccessElementSelector = createAddElementSelector();
    addSuccessBtnLi.appendChild(addSuccessElementSelector);
    successList.appendChild(addSuccessBtnLi);
    successDiv.appendChild(successHeader);
    successDiv.appendChild(successList);
    skillCheckContainer.appendChild(successDiv)
    // Failure branch
    const failureDiv = document.createElement('div');
    failureDiv.className = 'mt-2 w-full';
    const failureHeader = document.createElement('h4');
    failureHeader.className = 'font-semibold text-red-700';
    failureHeader.textContent = 'On Failure';
    const subList = document.createElement('ul');
    subList.className = "ml-2 mt-2 space-y-2 w-full"; // Indent and spac
    // Add button as a list item
    const addBtnLi = document.createElement('li');
    const addElementSelector = createAddElementSelector();
    addBtnLi.appendChild(addElementSelector);
    subList.appendChild(addBtnLi);
    failureDiv.appendChild(failureHeader);
    failureDiv.appendChild(subList);
    skillCheckContainer.appendChild(failureDiv)
    li.appendChild(skillCheckContainer);
}

function addChange(subLi) {
    // Row for label and remove button
    const row = document.createElement('div');
    row.className = "flex items-center justify-between";
    // Label
    const span = document.createElement('span');
    span.textContent = "Change";
    // Remove button
    const removeBtn = document.createElement('button');
    removeBtn.className = "text-red-500 hover:text-red-700 ml-2";
    removeBtn.title = "Remove";
    removeBtn.type = "button";
    removeBtn.innerHTML = "&times;";
    removeBtn.addEventListener('click', () => {
        subLi.remove();
    });
    // Assemble row
    row.appendChild(span);
    row.appendChild(removeBtn);
    subLi.appendChild(row);

    const descriptionContainer = document.createElement('div');
    descriptionContainer.className = 'ml-2 mt-2 p-2 border-l-2 border-slate-300 max-h-16';

    const textarea = document.createElement('textarea');
    textarea.className = 'w-full p-1 border border-slate-400 rounded-md text-sm max-h-14 ';
    textarea.rows = 4;
    textarea.placeholder = 'Enter description here...';

    descriptionContainer.appendChild(textarea);
    subLi.appendChild(descriptionContainer);
}

addTypeBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    addTypeDropdown.classList.remove('hidden')
});

addTypeDropdown.addEventListener('click', (e) => {
    const btn = e.target.closest('button[data-type]');
    if (btn) {
        const type = btn.getAttribute('data-type');
        // Add element to the encounter elements box
        if (encounterElementsPlaceholder) {
            encounterElementsPlaceholder.style.display = 'none';
        }
        if (encounterElementsList) {
            addSubEncounter(encounterElementsList, type);
        }
        addTypeDropdown.classList.add('hidden');
    }
});
function addSubEncounter(parentList, type) {
    const subLi = document.createElement('li');
    subLi.className = "bg-slate-200/30 border border-slate-300 w-full rounded px-3 py-2 mb-2";
    switch (type) {
        case "Skill Check":
            addSkillCheck(subLi);
            break;
            
        case "Description":
            addDescription(subLi);
            break;    
                
        case "Battle":
            addBattle(subLi);
            break;

        case "Change":
            addChange(subLi);
            break;

        default:
            // Row for label and remove button
            const row = document.createElement('div');
            row.className = "flex items-center justify-between";
            // Label
            const span = document.createElement('span');
            span.textContent = type;
            // Remove button
            const removeBtn = document.createElement('button');
            removeBtn.className = "text-red-500 hover:text-red-700 ml-2";
            removeBtn.title = "Remove";
            removeBtn.type = "button";
            removeBtn.innerHTML = "&times;";
            removeBtn.addEventListener('click', () => {
                subLi.remove();
            });
            // Assemble row
            row.appendChild(span);
            row.appendChild(removeBtn);
            subLi.appendChild(row);
            // If this type can have children, add a nested UL and Add Encounter button
            if (["",].includes(type)) {
                const subList = document.createElement('ul');
                subList.className = "ml-8 mt-2 space-y-2";
                // Add Encounter button (as a list item)
                const addBtnLi = document.createElement('li');
                const typeSelector = createAddElementSelector();
                addBtnLi.appendChild(typeSelector);
                subList.appendChild(addBtnLi); // Always keep this as the last <li>
                subLi.appendChild(subList);
            }
        break;
    }
    console.log(parentList.children)
    if (parentList.querySelector('button')) {
        parentList.insertBefore(subLi, parentList.lastElementChild);
    } else {
        parentList.appendChild(subLi);
    }
}

function createAddElementSelector() {
    const wrapper = document.createElement('div');
    const buttonWrapper = document.createElement('div');
    buttonWrapper.className = "relative"

    const selectBtn = document.createElement('button');
    selectBtn.className = "inline-flex justify-center items-center px-3 py-1 bg-slate-300 text-slate-800 rounded hover:bg-slate-400 text-sm";
    selectBtn.type = "button";
    selectBtn.textContent = "Add Element";

    
    const dropdown = document.createElement('div');
    dropdown.className = "origin-top-left absolute left-0 mt-2 w-40 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5 hidden z-40";
    dropdown.innerHTML = `
    <div class="py-1" role="menu">
    <button class="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-slate-100" data-type="Description">Description</button>
    <button class="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-slate-100" data-type="Battle">Battle</button>
    <button class="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-slate-100" data-type="Skill Check">Skill Check</button>
    <button class="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-slate-100" data-type="Change">Change</button>
    </div>
    `;
    selectBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        dropdown.classList.toggle('hidden');
    });
    
    dropdown.addEventListener('click', (e) => {
        const btn = e.target.closest('button[data-type]');
        e.stopPropagation();
        if (btn) {
            const type = btn.getAttribute('data-type');
            addSubEncounter(wrapper, type);
            dropdown.classList.add('hidden');
        }
    });
    
    // Hide dropdown when clicking outside
    document.addEventListener('click', (e) => {
        if (!selectBtn.contains(e.target) && !dropdown.contains(e.target)) {
            dropdown.classList.add('hidden');
        }
    });
    
    buttonWrapper.appendChild(selectBtn);
    buttonWrapper.appendChild(dropdown);
    wrapper.appendChild(buttonWrapper);
    return wrapper;
}