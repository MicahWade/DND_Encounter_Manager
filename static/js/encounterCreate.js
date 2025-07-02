var timeoutID;

document.querySelector('#search_input').addEventListener('input', function(e) {
  clearTimeout(timeoutID);
  timeoutID = setTimeout(function() {
    alert("1 second has passed since any input was received.");
    // doStuff()
  }, 1000);
});