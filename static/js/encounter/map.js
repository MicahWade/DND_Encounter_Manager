const mapSearch = document.getElementById('mapSearch');
const mapDropdown = document.getElementById('mapDropdown');
let debounceTimeout = null;
let mapSize = null;

const floorArrows = document.getElementById('floorArrows');
const arrowUp = document.getElementById('arrowUp');
const arrowDown = document.getElementById('arrowDown');
let currentFloors = [];
let currentFloorIndex = 0;
let currentMapTitle = null;
let mainMapPath = null;

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

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
    img.addEventListener('load', function handler() {
        this.removeEventListener('load', handler);
        addGridOverlay(this, mapSize)
    });
}

function addGridOverlay(img, size) {
    if (!img) return;
    let [cols, rows] = size.split('x').map(Number);
    if (isNaN(cols) || isNaN(rows) || cols <= 0 || rows <= 0) {
        console.error("Invalid grid size provided. Expected format 'WxH' (e.g., '10x8').");
        return;
    }

    // Create a canvas element
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');

    // Set canvas size based on image
    if (img.naturalHeight > img.naturalWidth) {
        canvas.height = img.width;
        canvas.width = img.height;
        ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
        [cols, rows] = [rows, cols]
    } else {
        canvas.width = img.width;
        canvas.height = img.height;
        ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
    }

    // Draw grid lines
    const cellWidth = canvas.width / cols;
    const cellHeight = canvas.height / rows;

    
    for (let i = 0; i <= cols; i++) {
        ctx.beginPath();
        ctx.moveTo(i * cellWidth, 0);
        ctx.lineTo(i * cellWidth, canvas.height);
        ctx.strokeStyle = 'rgba(0, 0, 0, 0.3)';
        ctx.stroke();
    }
    
    for (let j = 0; j <= rows; j++) {
        ctx.beginPath();
        ctx.moveTo(0, j * cellHeight);
        ctx.lineTo(canvas.width, j * cellHeight);
        ctx.strokeStyle = 'rgba(0, 0, 0, 0.3)';
        ctx.stroke();
    }
    
    ctx.rotate(Math.PI / 2);

    // Replace the original image with the canvas and keep its data
    const newImg = document.createElement('img');
    newImg.src = canvas.toDataURL('image/png');

    for (let i = 0; i < img.classList.length; i++) {
        newImg.classList.add(img.classList[i]);
    }
    newImg.id = img.id;
    newImg.alt = img.alt;
    img.parentNode.replaceChild(newImg, img);
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
    
    const mapContainer = document.getElementById('mapContainer');
    const img = document.createElement('img');
    img.src = `../static/${mainMapPath}`;
    img.alt = currentMapTitle || '';
    img.classList.add('max-w-full', 'max-h-full'); // Ensure image is contained
    rotateImageIfNeeded(img);

    // Clear previous image
    mapContainer.innerHTML = '';
    mapContainer.appendChild(img);
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
        
        // Fetch map info and  setimage
        try {
            const response = await fetch(`/map/get/${encodeURIComponent(title)}`);
            if (response.ok) {
                const mapInfo = await response.json();
                mainMapPath = mapInfo.image_path;
                mapSize = mapInfo.size; 
                if (mainMapPath) {
                    const img = document.getElementById('mapImage');
                    if (img) {
                        img.src = `../static/${mainMapPath}`;
                        img.alt = title;
                        rotateImageIfNeeded(img)
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