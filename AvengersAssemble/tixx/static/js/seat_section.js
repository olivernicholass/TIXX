const showGridButton = document.getElementById('section1');
const gridContainer = document.getElementById('gridContainer');

function showSection1AvailableSeats(){
  if (gridContainer.classList.contains('hidden')) {
    gridContainer.classList.remove('hidden');
    createGrid();
    alert("grid created");
  } else {
    gridContainer.classList.add('hidden');
    gridContainer.innerHTML = ''; // Clear the grid
  }
};

function createGrid() {
  for (let i = 0; i < 5; i++) {
    const row = document.createElement('div');
    row.classList.add('row');
    gridContainer.appendChild(row);
    for (let j = 0; j < 10; j++) {
      const seat = document.createElement('div');
      seat.classList.add('seat');
      gridContainer.appendChild(seat);
    }
  }
}