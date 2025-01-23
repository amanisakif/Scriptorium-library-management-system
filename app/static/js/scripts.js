// static/js/scripts.js
document.addEventListener('DOMContentLoaded', function() {
    let bookCarousel = document.getElementById('bookCarousel');
    if (bookCarousel) {
      let carousel = new bootstrap.Carousel(bookCarousel, {
        interval: 2000,
        wrap: true
      });
    }
  });
  