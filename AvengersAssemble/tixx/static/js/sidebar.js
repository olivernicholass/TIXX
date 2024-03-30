function openSidebar() {
    document.getElementById("mySidebar").style.width = "30%";
    document.body.classList.add("translucent");
}

function closeNav() {
    document.getElementById("mySidebar").style.width = "0";
    document.body.classList.remove("translucent");
}

document.getElementById('accountLink').addEventListener('click', openSidebar);