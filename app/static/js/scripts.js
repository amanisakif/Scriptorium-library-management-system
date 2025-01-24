// Initialize book carousel
document.addEventListener('DOMContentLoaded', function() {
  let bookCarousel = document.getElementById('bookCarousel');
  if (bookCarousel) {
      let carousel = new bootstrap.Carousel(bookCarousel, {
          interval: 2000,
          wrap: true
      });
  }
});

// Function to simulate data
function simulateData() {
  const simulateButton = document.getElementById('simulateButton');
  simulateButton.disabled = true;
  simulateButton.textContent = 'Simulating...';
  simulateButton.style.backgroundColor = '#ffc107'; // Yellow for simulation in progress

  fetch('/simulate-data')
      .then(response => response.text())
      .then(() => {
          simulateButton.textContent = 'Data Simulated!';
          simulateButton.style.backgroundColor = '#28a745'; // Green for success
          simulateButton.style.color = '#fff'; // White text for better contrast
      })
      .catch(error => {
          console.error('Error:', error);
          simulateButton.textContent = 'Error Simulating Data!';
          simulateButton.style.backgroundColor = '#dc3545'; // Red for failure
          simulateButton.style.color = '#fff';
      })
      .finally(() => {
          setTimeout(() => {
              simulateButton.disabled = false;
              simulateButton.textContent = 'Simulate Data';
              simulateButton.style.backgroundColor = ''; // Reset to default
              simulateButton.style.color = '';
          }, 3000); // Reset after 3 seconds
      });
}
