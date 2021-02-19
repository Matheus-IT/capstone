document.addEventListener('DOMContentLoaded', function() {
	const body = document.querySelector('body');
	
	const btnHamburger = body.querySelector('#btnHamburger');
	const mobileMenu = body.querySelector('#menuForMobile');
	const overlay = body.querySelector('#overlay');
	
	btnHamburger.addEventListener('click', function() {
		console.log('click');

		if (mobileMenu.classList.contains('menu--open'))
			handleCloseMenu();
		else
			handleOpenMenu();
	});

	function handleCloseMenu() {
		mobileMenu.classList.remove('menu--open');
		btnHamburger.classList.remove('navbar__toggle--open');
		body.classList.remove('noScroll');
		
		overlay.classList.remove('fade-in');
		overlay.classList.add('fade-out');

		for (const element of mobileMenu.children) {
			element.classList.remove('fade-in');
			element.classList.add('fade-out');
		}
	}

	function handleOpenMenu() {
		mobileMenu.classList.add('menu--open');
		btnHamburger.classList.add('navbar__toggle--open');
		body.classList.add('noScroll');

		overlay.classList.remove('fade-out');
		overlay.classList.add('fade-in');

		for (const element of mobileMenu.children) {
			element.classList.remove('fade-out');
			element.classList.add('fade-in');
		}
	}
});