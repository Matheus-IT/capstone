document.addEventListener('DOMContentLoaded', function () {
	const body = document.querySelector('body');

	const btnHamburger = body.querySelector('#btnHamburger');
	const mobileMenu = body.querySelector('#menuForMobile');
	const overlay = body.querySelector('#overlay');

	btnHamburger.addEventListener('click', function () {
		if (mobileMenu.classList.contains('mobile-menu--open'))
			handleCloseMenu();
		else
			handleOpenMenu();
	});

	function handleCloseMenu() {
		mobileMenu.classList.remove('mobile-menu--open');
		btnHamburger.classList.remove('navbar__toggle--open');
		body.classList.remove('noScroll');

		overlay.classList.remove('fade-in');
		overlay.classList.add('fade-out');
		overlay.style.display = 'none';

		for (const element of mobileMenu.children) {
			element.classList.remove('fade-in');
			element.classList.add('fade-out');
		}
	}

	function handleOpenMenu() {
		mobileMenu.classList.add('mobile-menu--open');
		btnHamburger.classList.add('navbar__toggle--open');
		body.classList.add('noScroll');

		overlay.classList.remove('fade-out');
		overlay.style.display = 'block';
		overlay.classList.add('fade-in');

		for (const element of mobileMenu.children) {
			element.classList.remove('fade-out');
			element.classList.add('fade-in');
		}
	}
});