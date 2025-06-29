const contentHTML = document.getElementById('content')
mainhtml = ""
function getEnemy(enemyID){
    fetch(`/enemy/${enemyID}`, {method: 'GET'})
        .then(response => {
            if (response.status == 200 || response.status == 201) {
                return response.text().then(html => {
                    mainhtml = contentHTML.innerHTML;
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