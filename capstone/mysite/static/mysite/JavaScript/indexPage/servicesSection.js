class Slider {
	buttonPrevious = document.querySelector('#navigationBtnLeft');
	buttonNext = document.querySelector('#navigationBtnRight');
	
	sliderContainer = document.querySelector('#slider');
	navigationTrackerItems = document.querySelector('#navigationTracker').children;
	slides = document.querySelector('#slides');
	currentSlide = 0; // Start on the first slide
	maxLengthOfSlides = 4;

	constructor() {
		this.buttonNext.onclick = this.handleGoToNextSlide;
		this.buttonPrevious.onclick = this.handleGoToPreviousSlide;
		this.sliderContainer.onscroll = this.handleScroll;
	}

	handleScroll = () => {
		const scrollOfOneCard = 338.5;
		const num = Math.ceil(this.sliderContainer.scrollLeft / scrollOfOneCard);
		for (let item of this.navigationTrackerItems) {
			item.classList.remove('item-active');
		}
		this.navigationTrackerItems[num].classList.add('item-active');
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
