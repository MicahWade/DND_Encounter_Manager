const mapSearch = document.getElementById('mapSearch');
const mapDropdown = document.getElementById('mapDropdown');
let debounceTimeout = null;

const floorArrows = document.getElementById('floorArrows');
const arrowUp = document.getElementById('arrowUp');
const arrowDown = document.getElementById('arrowDown');
let currentFloors = [];
let currentFloorIndex = 0;
let currentMapTitle = null;
let mainMapPath = null;

async function loadFloorsForMap() {
    // Fetch all floors for this map using the given path
    const floorResp = await fetch(`/map/floor/get/${encodeURIComponent(mainMapPath.split(".")[0])}`);
    if (!floorResp.ok) return;
    const floors = await floorResp.json();

    // Find current floor index
    let floorIdx = 0;
    if (Array.isArray(floors)) {
        floorIdx = floors.findIndex(f => f[1] === mainMapPath);
    }
    currentFloors = floors;
    currentFloorIndex = floorIdx >= 0 ? floorIdx : 0;
    updateFloorArrows();
}

function updateFloorArrows() {
    if (!currentFloors || currentFloors.length <= 1) {
        arrowUp.classList.add('hidden');
        arrowDown.classList.add('hidden');
        return;
    }
    // Show/hide up arrow
    if (currentFloorIndex < currentFloors.length - 1) {
        arrowUp.classList.remove('hidden');
    } else {
        arrowUp.classList.add('hidden');
    }
    // Show/hide down arrow
    if (currentFloorIndex > 0) {
        arrowDown.classList.remove('hidden');
    } else {
        arrowDown.classList.add('hidden');
    }
}

function setMapImageByFloor(idx) {
    if (!currentFloors[idx]) return;
    const [floorNumber, path] = currentFloors[idx];
    const img = document.querySelector('.content-center img');
    if (img) {
        img.src = `../static/${path}`;
        img.alt = currentMapTitle || '';
    }
}

arrowUp.addEventListener('click', (e) => {
    e.preventDefault();
    if (currentFloorIndex < currentFloors.length - 1) {
        currentFloorIndex++;
        setMapImageByFloor(currentFloorIndex);
        updateFloorArrows();
    }
});
arrowDown.addEventListener('click', (e) => {
    e.preventDefault();
    if (currentFloorIndex > 0) {
        currentFloorIndex--;
        setMapImageByFloor(currentFloorIndex);
        updateFloorArrows();
    }
});

// Fill input when clicking a dropdown item
mapDropdown.addEventListener('click', async (e) => {
    if (e.target && e.target.matches('div')) {
        const title = e.target.textContent;
        mapSearch.value = title;
        mapDropdown.classList.add('hidden');
        currentMapTitle = title;

        // Fetch map info and set image
        try {
            const response = await fetch(`/map/get/${encodeURIComponent(title)}`);
            if (response.ok) {
                const mapInfo = await response.json();
                console.log(mapInfo)
                mainMapPath = mapInfo.image_path;
                if (mainMapPath) {
                    // Find the image element in the content-center div
                    const img = document.querySelector('.content-center img');
                    if (img) {
                        img.src = `../static/${mainMapPath}`;
                        img.alt = title;
                    }
                    // Load floors and show arrows if needed
                    if (mapInfo.floor != 0){
                        await loadFloorsForMap();
                        setMapImageByFloor(currentFloorIndex);
                    } else {
                        // Clear floor data and hide arrows if no floors
                        currentFloors = [];
                        currentFloorIndex = 0;
                        arrowUp.classList.add('hidden');
                        arrowDown.classList.add('hidden');
                    }
                }
            }
        } catch (err) {
            // Optionally handle error
            console.error('Failed to fetch map info:', err);
        }
    }
});

mapSearch.addEventListener('input', () => {
    // Clear dropdown while typing
    mapDropdown.innerHTML = '';
    mapDropdown.classList.add('hidden');
    if (debounceTimeout) clearTimeout(debounceTimeout);

    const query = mapSearch.value.trim();
    if (!query) return;

    debounceTimeout = setTimeout(async () => {
        try {
            const response = await fetch(`/map/search/${encodeURIComponent(query)}`);
            if (!response.ok) {
                mapDropdown.classList.add('hidden');
                return;
            }
            const results = await response.json();
            // Accepts either array or object with 'maps' key
            const maps = Array.isArray(results) ? results : results.maps || [];
            if (maps.length > 0) {
                mapDropdown.innerHTML = maps.map(name =>
                    `<div class="p-2 hover:bg-slate-200 cursor-pointer">${name}</div>`
                ).join('');
                mapDropdown.classList.remove('hidden');
            } else {
                mapDropdown.innerHTML = '';
                mapDropdown.classList.add('hidden');
            }
        } catch (e) {
            mapDropdown.innerHTML = '';
            mapDropdown.classList.add('hidden');
        }
    }, 500);
});

// Hide dropdown when clicking outside
document.addEventListener('click', (e) => {
    if (!mapSearch.contains(e.target) && !mapDropdown.contains(e.target)) {
        mapDropdown.classList.add('hidden');
    }
});