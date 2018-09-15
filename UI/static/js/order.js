// Get the modal
var modal = document.getElementById('order');

var btn = document.getElementById('add-btn');

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}