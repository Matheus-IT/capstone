export function handleDisplayQueue(queueSize, queueContainer) {
	document.querySelector('#displayQueueSize').innerHTML = queueSize;
	queueContainer.innerHTML = '';

	for (let i = 0; i < queueSize; i++) {
		const person = createPerson();
		queueContainer.append(person);
	}
}

export function handleIncreaseQueue(queueContainer) {
	const domQueueSizeObj = document.querySelector('#displayQueueSize');
	let queueSize = Number.parseInt(domQueueSizeObj.innerHTML);
	queueSize++;
	domQueueSizeObj.innerHTML = queueSize;

	const person = createPersonWalking();
	queueContainer.append(person);

	person.onanimationend = function() {
		this.setAttribute('src', personWaitingSource);
	};
}

function createPersonWalking() {
	const personWalking = document.createElement('img');

	personWalking.setAttribute('src', personWalkingSource);
	personWalking.className = 'person';
	personWalking.classList.add('personArrivingWalking');
	return personWalking;
}

function createPerson() {
	const person = document.createElement('img');

	person.setAttribute('src', personWaitingSource);
	person.classList.add('person');
	return person;
}

export function handleDecreaseQueue(queueContainer) {
	const domQueueSizeObj = document.querySelector('#displayQueueSize');
	let queueSize = Number.parseInt(domQueueSizeObj.innerHTML);
	queueSize--;
	domQueueSizeObj.innerHTML = queueSize;

	const people = queueContainer.children;

	Array.from(people).forEach(person => {
		person.setAttribute('src', personWalkingSource);
	});

	const nextPerson = getNextElementDoesntContainClass(queueContainer, 'personWalkingAway');

	if (nextPerson) {
		nextPerson.classList.add('personWalkingAway');
	
		nextPerson.onanimationend = function() {
			nextPerson.remove();
	
			Array.from(people).forEach(person => {
				person.setAttribute('src', personWaitingSource);
			});
		};
	}
}

function getNextElementDoesntContainClass(container, className) {
	/**
	 * Returns the next element that doesn't have the give class
	 */
	let nextPerson = container.firstElementChild;

	if (nextPerson) {
		while (nextPerson.classList.contains(className)) {
			nextPerson = nextPerson.nextElementSibling;
		}
		return nextPerson;
	}
}
