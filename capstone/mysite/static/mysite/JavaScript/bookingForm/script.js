class MultiStepsForm {
	constructor() {
		this.currentPage = 0;
		this.slidePage = document.querySelector('.slide-page');
		
		this.nextButtons = document.querySelectorAll('.next');
		this.previousButtons = document.querySelectorAll('.prev');
		
		this.fields = document.querySelectorAll('.inputInf');
		
		this.progressCheck = document.querySelectorAll('.step__bullet .check');
		this.bullets = document.querySelectorAll('.step__bullet');
		
		this.submitBtn = document.querySelector('.submit');
	}
	
	get currentBullet() {
		return this.bullets[this.currentPage];
	}
	
	get currentNextButton() {
		return this.nextButtons[this.currentPage];
	}
	
	get currentProgressCheck() {
		return this.progressCheck[this.currentPage];
	}
	
	main() {
		this.nextButtons.forEach(nextBtn => {
			this.disableButton(nextBtn);
			nextBtn.onclick = this.handleGoNextStep;
		});
		
		this.fields.forEach(field => {
			field.onclick = this.handleFieldSelected;
		});
		
		this.previousButtons.forEach(prevBtn => {
			prevBtn.onclick = this.handleGoPreviousStep;
		});
		
		this.submitBtn.addEventListener('click', () => {
			this.currentBullet.classList.add('step__bullet--is-active');
			this.currentProgressCheck.classList.add('check--is-active');
			this.currentPage++;
			setTimeout(function() {
				alert('Your Form Successfully Signed up');
				location.reload();
			}, 1000);
		});
	}
	
	disableButton(btn) {
		btn.disabled = true;
		btn.classList.add('btns__btn--is-disabled');
	}
	
	handleGoNextStep = (event) => {
		event.preventDefault();
		this.currentBullet.classList.add('step__bullet--is-active');
		this.currentProgressCheck.classList.add('check--is-active');
		this.currentPage++;
		this.slidePage.style.marginLeft = `${(this.currentPage) * -25}%`;
	}
	
	handleGoPreviousStep = (event) => {
		event.preventDefault();
		this.currentPage--;
		this.slidePage.style.marginLeft = `${this.currentPage * -25}%`;
		this.currentBullet.classList.remove('step__bullet--is-active');
		this.currentProgressCheck.classList.remove('check--is-active');
	}
	
	handleFieldSelected = (event) => {
		this.currentNextButton.classList.remove('btns__btn--is-disabled');
		this.currentNextButton.disabled = false;
	}
}

document.addEventListener('DOMContentLoaded', function() {
	const multiStepsForm = new MultiStepsForm();
	multiStepsForm.main();
});
