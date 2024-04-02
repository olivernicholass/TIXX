// Update the figureImage + figureName to display
function updateSelectedFigure() {
    var figureId = document.getElementById("figure-Id").value;
    if (figureId) { 
        var figureName = document.getElementById("figure-Id").querySelector(`option[value="${figureId}"]`).text;
        var figureImage = getImage(figureId); 
        document.getElementById("selected-figure").style.display = "block"; 
        document.getElementById("selected-figure").innerHTML = `
            <img src="${figureImage}" alt="${figureName}">
            <p>${figureName.toUpperCase()}</p>
        `;
    } else {
        document.getElementById("selected-figure").style.display = "none"; 
    }
}

// FETCH the selected figureImage 
function getImage(figureName) {
    var options = document.querySelector(`#figure-Id option[value="${figureName}"]`);
    var figureImage = options.dataset.picture;
    return figureImage;
}

// Fill the event summary with details from the inputs
function updateSummary() {
    document.getElementById("eventName").textContent = document.getElementById("id_eventName").value;
    document.getElementById("eventDate").textContent = document.getElementById("id_eventDate").value;
    document.getElementById("eventTime").textContent = document.getElementById("id_eventTime").value;
    document.getElementById("eventLocation").textContent = document.getElementById("id_eventLocation").value;
    document.getElementById("eventDescription").textContent = document.getElementById("id_eventDescription").value;
    document.getElementById("eventGenre").textContent = document.getElementById("event-Genre").value;
    document.getElementById("arena").textContent = document.getElementById("arena-Id").selectedOptions[0].text;  
    document.getElementById("figure").textContent = document.getElementById("figure-Id").selectedOptions[0].text;  
}

// Display the Event Summary after the Organiser hits "Submit"
// The Organiser is forced to read their summary and then submit to Administration for review.
function showSummary(event) {
    event.preventDefault(); 
    updateSummary();
    document.getElementById("event-summary").style.display = "block";
    document.getElementById("send-admin").style.display = "block"; 
}

// Submit the form to admin_review
function submitForm(event) {
    event.preventDefault();
    document.querySelector(".event-form").submit();
}

document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("eventForm").addEventListener("input", updateSummary);
    document.addEventListener("click", function(event) {
        if (event.target.id === "send-admin") {
            submitForm(event);
        }
    });
});