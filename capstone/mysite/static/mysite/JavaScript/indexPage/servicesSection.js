class Slider {
  constructor() {
    this.sliderContainer = document.querySelector("#slider");
    this.sliderContainer.onscroll = this.handleScroll;

    // Buttons available for desktop design
    this.buttonPrevious = document.querySelector("#navigationBtnLeft");
    this.buttonPrevious.onclick = this.handleGoToPreviousSlide;

    this.buttonNext = document.querySelector("#navigationBtnRight");
    this.buttonNext.onclick = this.handleGoToNextSlide;

    // Tracker available for mobile design
    this.navigationTrackerItems =
      document.querySelector("#navigationTracker").children;

    this.slides = document.querySelector("#slides");

    this.currentSlide = 0; // The first slide starts on 0
    this.maxLengthOfSlides = 4;
  }

  handleScroll = () => {
    const scrollOfOneCard = 300; // In px

    const num = Math.ceil(this.sliderContainer.scrollLeft / scrollOfOneCard);
    for (let item of this.navigationTrackerItems) {
      item.classList.remove("item-active");
    }
    this.navigationTrackerItems[num].classList.add("item-active");
  };

  handleGoToNextSlide = () => {
    if (this.currentSlide < this.maxLengthOfSlides) {
      this.currentSlide++;
      this.moveToSlide(this.currentSlide);
    }
  };

  handleGoToPreviousSlide = () => {
    if (this.currentSlide > 0) {
      this.currentSlide--;
      this.moveToSlide(this.currentSlide);
    }
  };

  moveToSlide(slideNum) {
    const currentMarginLeft = -(slideNum * 100);
    this.slides.style.marginLeft = `${currentMarginLeft}%`;
  }
}

document.addEventListener("DOMContentLoaded", function () {
  const slider = new Slider();
});
