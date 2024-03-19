
// Displays currently active item in the navbar.
// I.e if Events is selected it will be underlined.

document.addEventListener("DOMContentLoaded", function() {
    const items = document.querySelectorAll('.nav-link');

    items.forEach(function(link) {
        link.addEventListener('click', function() {
            items.forEach(function(navLink) {
                navLink.classList.remove('active');
            });
            link.classList.add('active');
        });
    });


    // Extra formatting for event displaying

    const eventCharacters = document.querySelectorAll('#eventDate');
    eventCharacters.forEach(function(eventDateElement) {
        const eventDate = eventDateElement.textContent.trim();
        const [month, day, year] = eventDate.split(/[\s,]+/); 
        eventDateElement.innerHTML = `<span class="month">${month}</span> <span class="day">${day}</span><br>• ${year}`;
    });



// Functionality for the countdown timer.
function countdown() {
    const eventDates = document.querySelectorAll('#eventDate');
    const eventTimes = Array.from(eventDates).map(dateElem => {
        const eventDateString = dateElem.textContent.trim();
        const eventClean = eventDateString.replace(/[^\w\s]/g, '');
        const eventdt = new Date(eventClean);
        const time = eventdt.getTime();
        return time - Date.now();
    });

    const filter = eventTimes.filter(time => !isNaN(time));
    let nearest = 0;
    let nearestDiff = filter[0];

    for (let i = 1; i < filter.length; i++) {
        if (Math.abs(filter[i]) < Math.abs(nearestDiff)) {
            nearest = i;
            nearestDiff = filter[i];
        }
    }

    const countdown = Math.abs(filter[nearest]);
    const days = Math.floor(countdown / (1000*60*60*24));
    const hours = Math.floor((countdown % (1000*60*60*24)) / (1000*60*60));
    const minutes = Math.floor((countdown % (1000*60*60)) / (1000*60));
    const seconds = Math.floor((countdown % (1000*60)) / 1000);

    document.getElementById('days').querySelector('.cv').textContent = days.toString().padStart(2, '0');
    document.getElementById('hours').querySelector('.cv').textContent = hours.toString().padStart(2, '0');
    document.getElementById('minutes').querySelector('.cv').textContent = minutes.toString().padStart(2, '0');
    document.getElementById('seconds').querySelector('.cv').textContent = seconds.toString().padStart(2, '0');
}

countdown();

setInterval(countdown, 1000);
});
