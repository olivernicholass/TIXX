document.addEventListener("DOMContentLoaded", function() {

    // MODAL to appear when user selects "TERMS and CONDITIONS"
    
    var modal = document.getElementById("termsModal");
    var terms = document.getElementById("conditions");
    var exit = document.getElementsByClassName("close")[0];

    terms.onclick = function() {
        modal.style.display = "block";
    }

    exit.onclick = function() {
        modal.style.display = "none";
    }

    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }
});