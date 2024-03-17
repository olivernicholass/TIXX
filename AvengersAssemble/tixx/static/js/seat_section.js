document.getElementById("section1").addEventListener("click", function() {
    var table = document.getElementById("section1table");
    console.log("1");
    if (table.style.display === "none") {
        table.style.display = "block";
    } else {
        table.style.display = "none";
    }
});