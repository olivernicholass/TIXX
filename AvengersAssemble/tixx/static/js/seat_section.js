const showGridButton = document.getElementById('section1');
const gridContainer = document.getElementById('gridContainer');
let ticketData = []

fetch('/get-ticket-data/')
  .then(response => response.json())
  .then(data => {
    // Handle the received data
    ticketData = data.tickets;
    console.log(ticketData);
  })
  .catch(error => {
    console.error('Error:', error);
  });

function showSection1AvailableSeats(zone){
  var rowsize = 0;
  var colsize = 0;
  switch(zone){
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

      // seat.addEventListener('click', function(){
      //   seat.classList.toggle('selected');
      //   updateSelectedSeats();
      // })
    }
  }
}

function updateSelectedSeats(){
  const selectedSeatsList = document.getElementById('selected-seats');
  selectedSeatsList.innerHTML = ''; // Clear previous selection
  
  // Get all selected seats
  const selectedSeats = document.querySelectorAll('.seat.selected');
  
  // Create list items for selected seats
  selectedSeats.forEach(function(seat) {
    const listItem = document.createElement('li');
    listItem.textContent = 'Row ' + (seat.parentElement.rowIndex + 1) + ', Seat ' + (seat.cellIndex + 1);
    selectedSeatsList.appendChild(listItem);
  });
}

gridContainer.addEventListener('click', (e) => {
  if(e.target.classList.contains('seat') && !e.target.classList.contains('occupied')){
    e.target.classList.toggle('selected');
    alert('hello');
  }
});