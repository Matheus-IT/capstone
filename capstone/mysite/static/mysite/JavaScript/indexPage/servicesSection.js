class Slider {
	buttonPrevious = document.querySelector('#navigationBtnLeft');
	buttonNext = document.querySelector('#navigationBtnRight');
	
	slides = document.querySelector('#slides');
	currentSlide = 0; // Start on the first slide
	maxLengthOfSlides = 4;

	constructor() {
		this.buttonNext.onclick = this.handleGoToNextSlide;
		this.buttonPrevious.onclick = this.handleGoToPreviousSlide;
	}
	
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


document.addEventListener('DOMContentLoaded', function() {
	const slider = new Slider();
});
