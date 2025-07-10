const mapSearch = document.getElementById('mapSearch');
const mapDropdown = document.getElementById('mapDropdown');
let debounceTimeout = null;
let mapSize = null;

const floorArrows = document.getElementById('floorArrows');
const arrowUp = document.getElementById('arrowUp');
const arrowDown = document.getElementById('arrowDown');
const mapContainer = document.getElementById('mapContainer')
let floorImages = [];
let floorObjects = [];
let currentFloorIndex = 0;
let currentMapTitle = null;
let mainMapPath = null;

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}
function highlightMapEntities(entities, floorIndex = 0) {
    const img = floorImages[floorIndex];
    if (!img) return;

    // Retrieve the grid size for the current map
    const size = mapSize;
    const [cols, rows] = size.split('x').map(Number);

    // Create a new canvas and draw the image
    const canvas = document.createElement('canvas');
    canvas.width = img.width;
    canvas.height = img.height;
    const ctx = canvas.getContext('2d');
    ctx.drawImage(img, 0, 0, canvas.width, canvas.height);

    // Define color mappings based on entity type
    const colorMap = {
        'level up': 'rgba(0, 255, 0, 0.3)', // Green
        'entity': 'rgba(255, 0, 0, 0.3)',   // Red
        'shopkeeper': 'rgba(0, 0, 255, 0.3)', // Blue
        default: 'rgba(255, 255, 0, 0.3)'  // Yellow
    };

    // Process each entity
    entities.forEach(([type, x, y, data]) => {
        const cellWidth = canvas.width / cols;
        const cellHeight = canvas.height / rows;

        const color = colorMap[type] || colorMap.default;
        ctx.fillStyle = color;
        ctx.fillRect(x * cellWidth, y * cellHeight, cellWidth, cellHeight);
    });

    // Replace the image with the new canvas
    img.src = canvas.toDataURL('image/png');
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
    currentFloorIndex = floorIdx >= 0 ? floorIdx : 0;

    floors.forEach(element => {
        fetch(`../map/objects/get/${element[1]}`)
        .then(response => {
            if (!response.ok) throw new Error("Network response was not ok");
            return response.json();
        })
        .then(data => {
            floorObjects[element[0] - 1] = data;
            // console.log(data);
            highlightMapEntities(data, element[0] - 1)
        })
        .catch(error => {
            console.error("Error fetching map data:", error);
        });
        if(element[1] != mainMapPath){
            const img = document.createElement('img');
            img.classList.add('hidden');
            img.src = `../static/${element[1]}`;
            img.classList = 'max-w-full max-h-full object-contain ';
            mapContainer.appendChild(img);
            img.addEventListener('load', function handler() {
                img.removeEventListener('load', handler);
                addGridOverlay(img, element[2], true, element[0] - 1 );
            });
        }
    });

    updateFloorArrows();
}

function clear() {
    floorImages.forEach(element => {
        if (element.id != "mapImage0") {
            element.remove()
        }
    });
}

function addGridOverlay(img, size, hidden = false, floorIndex = 0) {
    if (!img) return;
    let [cols, rows] = size.split('x').map(Number);
    if (isNaN(cols) || isNaN(rows) || cols <= 0 || rows <= 0) {
        console.error("Invalid grid size provided. Expected format 'WxH' (e.g., '10x8').");
        return;
    }

    // Create a canvas element
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    canvas.width = img.width;
    canvas.height = img.height;
    ctx.drawImage(img, 0, 0, canvas.width, canvas.height);

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

    // Replace the original image with the canvas and keep its data
    const newImg = document.createElement('img');
    newImg.src = canvas.toDataURL('image/png');

    for (let i = 0; i < img.classList.length; i++) {
        newImg.classList.add(img.classList[i]);
    }

    // Position absolutely and set z-index
    if (hidden) {
        newImg.id = `mapImage${floorIndex}`;
        newImg.classList.add('hidden');
        floorImages[floorIndex] = newImg;
        newImg.classList.add('absolute', 'left-0', 'top-0', 'w-full', 'h-full', `z-[${floorIndex}]`);
    } else {
        newImg.id = `mapImage${currentFloorIndex}`;
        floorImages[currentFloorIndex] = newImg;
    }

    newImg.alt = img.alt;
    img.parentNode.replaceChild(newImg, img);
}
function updateFloorArrows() {
    if (!floorImages || floorImages.length <= 1) {
        arrowUp.classList.add('hidden');
        arrowDown.classList.add('hidden');
        return;
    }
    if (currentFloorIndex < floorImages.length - 1) {
        arrowUp.classList.remove('hidden');
    } else {
        arrowUp.classList.add('hidden');
    }
    if (currentFloorIndex > 0) {
        arrowDown.classList.remove('hidden');
    } else {
        arrowDown.classList.add('hidden');
    }
}

function setMapImageByFloor(idx, hidden) {
    if (!floorImages[idx]) return;
    img = floorImages[idx];
    if (hidden){
        img.classList.add('hidden')
    } else{
        img.classList.remove('hidden')
    }
}

arrowUp.addEventListener('click', (e) => {
    e.preventDefault();
    if (currentFloorIndex < floorImages.length - 1) {
        currentFloorIndex++;
        setMapImageByFloor(currentFloorIndex, false);
        updateFloorArrows();
    }
});
arrowDown.addEventListener('click', (e) => {
    e.preventDefault();
    if (currentFloorIndex > 0) {
        setMapImageByFloor(currentFloorIndex, true);
        currentFloorIndex--;
        updateFloorArrows();
    }
});

// Fill input when clicking a dropdown item
mapDropdown.addEventListener('click', async (e) => {
    const itemDiv = e.target.closest('div.p-2');
    if (itemDiv && mapDropdown.contains(itemDiv)) {
        const title = itemDiv.querySelector('span').textContent;
        mapSearch.value = title;
        mapDropdown.classList.add('hidden');
        currentMapTitle = title;

        try {
            const response = await fetch(`/map/get/${encodeURIComponent(title)}`);
            if (response.ok) {
                const mapInfo = await response.json();
                mainMapPath = mapInfo.image_path;
                mapSize = mapInfo.size;
                if (mainMapPath) {
                    clear()
                    floorImages = new Array(mapInfo.floor + 1);
                    floorObjects = new Array(mapInfo.floor + 1);
                    const img = document.getElementById('mapImage0');
                    if (img) {
                        img.src = `../static/${mainMapPath}`;
                        img.alt = title;
                        img.addEventListener('load', function handler() {
                            this.removeEventListener('load', handler);
                            addGridOverlay(this, mapSize);
                        });
                    }
                    if (mapInfo.floor != 0) {
                        await loadFloorsForMap(); // Load all floors and render them
                    } else {
                        currentFloorIndex = mapInfo.floor;
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