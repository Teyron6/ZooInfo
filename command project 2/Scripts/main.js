let currentIndex = 0;
const slides = document.querySelectorAll('.fact_day');
const slideInterval = 3000;
 
function changeSlide() {
  slides[currentIndex].style.opacity = 0;
  currentIndex = (currentIndex + 1) % slides.length;
  slides[currentIndex].style.opacity = 1;
}
 
setInterval(changeSlide, slideInterval);