const mapSearch = document.getElementById('mapSearch');
const mapDropdown = document.getElementById('mapDropdown');
let debounceTimeout = null;

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

// Fill input when clicking a dropdown item
mapDropdown.addEventListener('click', async (e) => {
    if (e.target && e.target.matches('div')) {
        const title = e.target.textContent;
        mapSearch.value = title;
        mapDropdown.classList.add('hidden');

        // Fetch map info and set image
        try {
            const response = await fetch(`/map/get/${encodeURIComponent(title)}`);
            if (response.ok) {
                const mapInfo = await response.json();
                // Adjust property name if needed
                const imagePath = mapInfo.image_path || mapInfo.path || mapInfo.img || null;
                if (imagePath) {
                    // Find the image element in the content-center div
                    const img = document.querySelector('.content-center img');
                    if (img) {
                        img.src = `../static/${imagePath}`;
                        img.alt = title;
                    }
                }
            }
        } catch (err) {
            // Optionally handle error
            console.error('Failed to fetch map info:', err);
        }
    }
});