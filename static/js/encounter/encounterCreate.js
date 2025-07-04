const encounterElementsBox = document.getElementById('encounterElementsBox');
const encounterElementsList = document.getElementById('encounterElementsList');
const encounterElementsPlaceholder = document.getElementById('encounterElementsPlaceholder');
const addTypeListItem = document.getElementById('addTypeListItem');
const addTypeBtn = document.getElementById('addTypeBtn');
const addTypeDropdown = document.getElementById('addTypeDropdown');

if (addTypeBtn && addTypeDropdown) {
    addTypeBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    addTypeDropdown.classList.remove('hidden')
    });

    addTypeDropdown.addEventListener('click', (e) => {
        console.log("drop")
        const btn = e.target.closest('button[data-type]');
        if (btn) {
            const type = btn.getAttribute('data-type');
            // Add element to the encounter elements box
            if (encounterElementsPlaceholder) {
                encounterElementsPlaceholder.style.display = 'none';
            }
            if (encounterElementsList) {
                const li = document.createElement('li');
                li.className = "bg-slate-100 rounded px-3 py-2 mb-2";

                // Main row (flex for parent)
                const row = document.createElement('div');
                row.className = "flex items-center justify-between";

                const span = document.createElement('span');
                span.textContent = type;

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

                // For types with sub-encounters
                if (["Battle", "Skill Check", "Change"].includes(type)) {
                    // Nested UL
                    const subList = document.createElement('ul');
                    subList.className = "ml-8 mt-2 space-y-2"; // Indent and spacing

                    // Add button as a list item
                    const addBtnLi = document.createElement('li');
                    const addElementSelector = createAddElementSelector((subType) => {
                        addSubEncounter(subList, subType);
                    });
                    addBtnLi.appendChild(addElementSelector);
                    subList.appendChild(addBtnLi);

                    li.appendChild(subList);
                }

                // Insert above the Add to Encounter button
                encounterElementsList.insertBefore(li, addTypeListItem);
            }
            addTypeDropdown.classList.add('hidden');
        }

    });

    function addSubEncounter(parentList, type) {
        // Create the sub-list item
        const subLi = document.createElement('li');
        subLi.className = "bg-slate-100 rounded px-3 py-2 mb-2";

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
        if (["Battle", "Skill Check", "Change"].includes(type)) {
            const subList = document.createElement('ul');
            subList.className = "ml-8 mt-2 space-y-2";

            // Add Encounter button (as a list item)
            const addBtnLi = document.createElement('li');
            const typeSelector = createAddElementSelector((subType, wrapper) => {
                addSubEncounter(subList, subType);
            });
            addBtnLi.appendChild(typeSelector);
            subList.appendChild(addBtnLi); // Always keep this as the last <li>

            subLi.appendChild(subList);
        }

        // If the parent list already has an "Add Encounter" button as the last <li>, insert before it
        // Otherwise, just append (should only happen at initial creation)
        if (
            parentList.lastElementChild &&
            parentList.lastElementChild.querySelector &&
            parentList.lastElementChild.querySelector('button')
        ) {
            parentList.insertBefore(subLi, parentList.lastElementChild);
        } else {
            parentList.appendChild(subLi);
        }
    }
}

function createAddElementSelector(onSelect) {
    console.log("element")
    const wrapper = document.createElement('div');
    wrapper.className = "relative inline-block";

    const selectBtn = document.createElement('button');
    selectBtn.className = "inline-flex items-center px-3 py-1 bg-slate-300 text-slate-800 rounded hover:bg-slate-400 text-sm";
    selectBtn.type = "button";
    selectBtn.textContent = "Add Encounter";

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
            onSelect(type, wrapper);
            dropdown.classList.add('hidden');
        }
    });

    // Hide dropdown when clicking outside
    document.addEventListener('click', (e) => {
        if (!selectBtn.contains(e.target) && !dropdown.contains(e.target)) {
            dropdown.classList.add('hidden');
        }
    });

    wrapper.appendChild(selectBtn);
    wrapper.appendChild(dropdown);
    return wrapper;
}