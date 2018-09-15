var modal = document.getElementById('addFood');
var btn = document.getElementById('add-food-btn');

var modal = document.getElementById('editFood');
var btn = document.getElementById('edit-food-btn');
// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}

