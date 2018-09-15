// Get the modal
var modal = document.getElementById('signup');

var btn = document.getElementById('btn');

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}