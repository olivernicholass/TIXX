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
  for (let i = 0; i < rowsize; i++) {
    const row = document.createElement('div');
    row.classList.add('row');
    row.classList.add('seatcontainer');
    gridContainer.appendChild(row);
    for (let j = 0; j < colsize; j++) {
      const seat = document.createElement('div');
      seat.classList.add('seat');
      row.appendChild(seat);
    }
  }
}

gridContainer.addEventListener('click', (e) => {
  if(e.target.classList.contains('seat') && !e.target.classList.contains('occupied')){
    e.target.classList.toggle('selected');
    
  }
});