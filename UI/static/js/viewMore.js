// Get the modal
var modal = document.getElementById('food');

var btn = document.getElementById('view');

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}