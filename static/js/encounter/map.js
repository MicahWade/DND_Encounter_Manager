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

function rotateImageIfNeeded(img) {
    if (!img) return;
    img.style.transform = '';
    img.style.maxWidth = '';
    img.style.maxHeight = '';
    img.style.width = '';
    img.style.height = '';
    img.addEventListener('load', function handler() {
        img.removeEventListener('load', handler);
        const parent = img.parentElement;
        const parentRect = parent.getBoundingClientRect();
        if (img.naturalHeight > img.naturalWidth) {
            img.style.transform = 'translate(-50%, -50%) rotate(90deg)';
            img.style.maxWidth = `${parentRect.height}px`;
            img.style.maxHeight = `${parentRect.width}px`;
        } else {
            img.style.transform = 'translate(-50%, -50%)';
            img.style.maxWidth = `${parentRect.width}px`;
            img.style.maxHeight = `${parentRect.height}px`;
        }
        img.style.position = 'absolute';
        img.style.left = '50%';
        img.style.top = '50%';
    });
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
        img.src = `../static/${mainMapPath}`;
        img.alt = currentMapTitle || '';
        rotateImageIfNeeded(img);
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
    // Find the closest dropdown item div
    const itemDiv = e.target.closest('div.p-2');
    if (itemDiv && mapDropdown.contains(itemDiv)) {
        const title = itemDiv.querySelector('span').textContent;
        mapSearch.value = title;
        mapDropdown.classList.add('hidden');
        currentMapTitle = title;

        // Fetch map info and set image
        try {
            const response = await fetch(`/map/get/${encodeURIComponent(title)}`);
            if (response.ok) {
                const mapInfo = await response.json();
                mainMapPath = mapInfo.image_path;
                if (mainMapPath) {
                    const img = document.querySelector('.content-center img');
                    if (img) {
                        img.src = `../static/${mainMapPath}`;
                        img.alt = title;
                        rotateImageIfNeeded(img);
                    }
                    if (mapInfo.floor != 0){
                        await loadFloorsForMap();
                        setMapImageByFloor(currentFloorIndex);
                    } else {
                        currentFloors = [];
                        currentFloorIndex = 0;
                        arrowUp.classList.add('hidden');
                        arrowDown.classList.add('hidden');
                    }
                }
            }
        } catch (err) {
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
                mapDropdown.innerHTML = maps.map(map => {
                    const thumbPath = `../static/${map[1].replace("images", "thumbnails") .split(".")[0] + ".webp"}`;
                    return `
                        <div class="p-2 hover:bg-slate-200 cursor-pointer flex items-center justify-between">
                            <span>${map[0]}</span>
                            <img src="${thumbPath}" alt="thumbnail" class="h-6 w-auto ml-2 rounded shadow" style="max-height:1.5em;">
                        </div>
                    `;
                }).join('');
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