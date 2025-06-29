const contentHTML = document.getElementById('content');
const defultSearch = document.getElementById('enemy-list').innerHTML;
const baseHTML = contentHTML.innerHTML;
function getEnemy(enemyID){
    fetch(`/enemy/${enemyID}`, {method: 'GET'})
        .then(response => {
            if (response.status == 200 || response.status == 201) {
                return response.text().then(html => {
                    contentHTML.innerHTML = html;
                });
            } else if (response.status == 404){
                return response.text().then(text => {
                    alert(text); // Alert the user with the error message
                });
            } else{
                alert("an error occurred please try again or mabye later");
            }
        });
}
function goback(){

}

function searchEnemy() {
    const term = document.getElementById("enemy-search").value.trim().toLowerCase();
    if (term == '' || term == ' '){
        document.getElementById('enemy-list').innerHTML = defultSearch;
    }
    else{
        fetch(`/search/enemy/${encodeURIComponent(term)}`, {method: 'GET'})
            .then(response => response.json())
            .then(data => {
                // data should be { enemys: [...] }
                const enemys = data.enemys || [];
                const enemyList = document.getElementById('enemy-list');
                enemyList.innerHTML = '';
                enemys.forEach(item => {
                    // item: [name, CR, id]
                    const div = document.createElement('div');
                    div.className = "px-6 py-3";
                    div.innerHTML = `
                        <button class="w-full" onclick="getEnemy(${item[2]})">
                            <div class="justify-between items-center w-full grid grid-cols-2">
                                <span class="text-left text-gray-900 hover:text-sky-300 text-left">${item[0]}</span>
                                <span class="text-left text-gray-900 text-right">${item[1]}</span>
                            </div>
                        </button>
                    `;
                    enemyList.appendChild(div);
                });
            });
    }
}