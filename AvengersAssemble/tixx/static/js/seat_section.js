const showGridButton = document.getElementById('section1');
const gridContainer = document.getElementById('gridContainer');
const eventIdElement = document.getElementById('eventId');
const eventid = eventIdElement.textContent;

let ticketData = [];
let selectedSeats = [];




function showSection1AvailableSeats(zone) {
  var rowsize = 0;
  var colsize = 0;
  switch (zone) {
    case 1:
      rowsize = 10;
      colsize = 50;
      break;
    case 2:
      rowsize = 10;
      colsize = 50;
      break;
    case 3:
      rowsize = 20;
      colsize = 10;
      break;
    case 4:
      rowsize = 20;
      colsize = 10;
      break;
  }

  gridContainer.innerHTML = ''; // Clear the grid
  createGrid(zone, rowsize, colsize);
  console.log("grid created");

};

function createGrid(zone, rowsize, colsize) {

  const zoneNumber = document.createElement('p');
  zoneNumber.textContent = "Section " + zone + " seats:";
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
      seat.classList.add('seat');
      rowElement.appendChild(seat);

      const seatLabel = "S" + zone + alphabet.charAt(row) + (col + 1);
      seat.setAttribute('data-seat-label', seatLabel);
    }
  }
}

function addSelectedSeats(seatLabel) {
  console.log('seat selected: ' + seatLabel);

  const selectedSeatsList = document.getElementById('selected-seats');

  // Create list items for selected seats
  const listItem = document.createElement('li');
  listItem.textContent = 'seat selected: ' + seatLabel;
  listItem.setAttribute('data-seat-label', seatLabel);
  selectedSeatsList.appendChild(listItem);

  selectedSeats.push(seatLabel);
}

function removeSelectedSeat(seatLabel) {
  console.log('seat deselected: ' + seatLabel);

  const selectedSeatsList = document.getElementById('selected-seats');
  const listItemToRemove = selectedSeatsList.querySelector(`li[data-seat-label="${seatLabel}"]`);
  // Find the list item with the deselected seat label and remove it
  if (listItemToRemove) {
    selectedSeatsList.removeChild(listItemToRemove);
  }
  console.log('Seat Label:', seatLabel);
  console.log('Selected Seats List:', selectedSeatsList);
  console.log('List Item to Remove:', listItemToRemove);

  // Remove the deselected seat label from the global array
  selectedSeats = selectedSeats.filter(label => label !== seatLabel);
}

gridContainer.addEventListener('click', (e) => {
  if (e.target.classList.contains('seat') && !e.target.classList.contains('occupied')) {
    const seatLabel = e.target.getAttribute('data-seat-label');
    const isSelected = e.target.classList.toggle('selected');

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