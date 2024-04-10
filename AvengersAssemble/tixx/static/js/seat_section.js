const showGridButton = document.getElementById('section1');
const gridContainer = document.getElementById('gridContainer');
const eventIdElement = document.getElementById('eventId');
const eventid = eventIdElement.textContent;

let ticketData = [];
let selectedSeats = [];

// Add an event listener for the DOMContentLoaded event
document.addEventListener('DOMContentLoaded', function () {
  ticketData = JSON.parse(document.getElementById('ticketsData').getAttribute('data-tickets'));
  //console.log("TicketData: " + ticketData);
});

var total = 0;

function showSection1AvailableSeats(zone) {
  var rowsize = 0;
  var colsize = 0;
  switch (zone) {
    case 1:
      rowsize = 25;
      colsize = 25;
      break;
    case 2:
      rowsize = 25;
      colsize = 25;
      break;
    case 3:
      rowsize = 25;
      colsize = 25;
      break;
    case 4:
      rowsize = 25;
      colsize = 25;
      break;
  }

  gridContainer.innerHTML = ''; // Clear the grid
  createGrid(zone, rowsize, colsize);
  console.log("grid created");

};

function createGrid(zone, rowsize, colsize) {

  const zoneNumber = document.createElement('p');
  zoneNumber.textContent = "Section " + zone + " seats:";
  zoneNumber.classList.add('seatcontainer');
  gridContainer.appendChild(zoneNumber);

  const alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';

  for (let row = 0; row < rowsize; row++) {

    // Create a row for the seats
    const rowElement = document.createElement('div');
    rowElement.classList.add('row', 'seatcontainer');
    gridContainer.appendChild(rowElement);

    // Add seats to the row
    for (let col = 0; col < colsize; col++) {

      const seat = document.createElement('div');
      const seatLabel = "S" + zone + alphabet.charAt(row) + (col + 1);

      seat.classList.add('seat');
      if (!available(seatLabel)) {
        seat.classList.add('occupied');
      }

      rowElement.appendChild(seat);

      seat.setAttribute('data-seat-label', seatLabel);

    }
  }
}

function available(seatLabel) {
  ticket = ticketData.find(ticket => ticket.seatNum === seatLabel);
  //console.log(ticket);
  return ticket.available;
}

function addSelectedSeats(seatLabel) {
  console.log('seat selected: ' + seatLabel);

  const selectedSeatsDiv = document.getElementById('selected-seats');
  ticket = ticketData.find(ticket => ticket.seatNum === seatLabel);
  // Create card element to display ticket information
  const card = document.createElement('div');
  card.classList.add('card', 'mb-3');
  card.setAttribute('data-seat-label', seatLabel);
  // Create card body
  const cardBody = document.createElement('div');
  cardBody.classList.add('card-body');

  // Populate card body with ticket information
  const ticketInfo = `
    <h5 class="card-title">${ticket.ticketType}</h5>
    <p class="card-text">Seat Label: ${ticket.seatNum}</p>
    <p class="card-text">Price: $${ticket.ticketPrice}</p>
  `;
  cardBody.innerHTML = ticketInfo;

  // Append card body to card
  card.appendChild(cardBody);

  // Append card to selected-seats div
  selectedSeatsDiv.appendChild(card);
  selectedSeats.push(seatLabel);

  
  updateSubtotal(true, ticket.ticketPrice);

}

function removeSelectedSeat(seatLabel) {
  console.log('seat deselected: ' + seatLabel);

  const selectedSeatsList = document.getElementById('selected-seats');
  ticket = ticketData.find(ticket => ticket.seatNum === seatLabel);
  // Find card elements with the deselected seat label and remove them
  const cardsToRemove = selectedSeatsList.querySelectorAll(`.card[data-seat-label="${seatLabel}"]`);
  cardsToRemove.forEach(card => {
    selectedSeatsList.removeChild(card);
  });

  console.log('Seat Label:', seatLabel);
  console.log('Selected Seats List:', selectedSeatsList);
  console.log('Cards to Remove:', cardsToRemove);

  // Remove the deselected seat label from the global array
  selectedSeats = selectedSeats.filter(label => label !== seatLabel);

  updateSubtotal(false, ticket.ticketPrice);
}




function updateSubtotal(added, price) {
  if(added){
    total += price;
  }else{
    total -= price;
  }
  // Calculate subtotal based on ticketsData array and update subtotal element
  const subtotalElement = document.getElementById('subtotal');
  console.log(total.toFixed(2));
  subtotalElement.textContent = `Subtotal: $${total.toFixed(2)}`; // Format subtotal to two decimal places
}


gridContainer.addEventListener('click', (e) => {
  if (e.target.classList.contains('seat') && !e.target.classList.contains('occupied')) {
    const seatLabel = e.target.getAttribute('data-seat-label');
    const isSelected = e.target.classList.toggle('selected');
    
    console.log(selectedSeats);

    if (isSelected) {
      addSelectedSeats(seatLabel);
    } else {
      removeSelectedSeat(seatLabel);
    }
  }
});




document.getElementById('checkoutButton').addEventListener('click', function () {

  console.log("Event ID: ", eventid);

  // Check if selectedSeats array is empty
  if (selectedSeats.length === 0) {
    // Display an error message or perform any other action to handle the empty selectedSeats array

    return; // Exit the event listener function
  }

  // Send the selectedSeats array to the server using fetch API
  fetch('/checkout/' + eventid + '/' + selectedSeats.join(',') + '/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken'), // Include the CSRF token in the headers
    },
    body: JSON.stringify({ selectedSeats: selectedSeats }),
  }).then(response => {
    if (response.ok) {
      // If the response is successful, redirect to the checkout page
      window.location.href = '/checkout/' + eventid + '/' + selectedSeats.join(',') + '/';
    } else {
      // Handle error if needed
      console.error('Error occurred while processing checkout.');
    }
  }).catch(error => {
    console.error('Error occurred while processing checkout:', error);
  });
});

// Function to get CSRF token from cookie
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}