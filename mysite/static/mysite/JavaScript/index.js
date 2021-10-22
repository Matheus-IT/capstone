import * as handleQueue from './handleQueue.js';


document.addEventListener('DOMContentLoaded', function() {
	const roomName = document.getElementById('room-name').innerText;
	const queueContainer = document.querySelector('#queueContainer');

	let socket;
	handleSocketClose();

	function handleSocketClose(event) {
		/**
		 * Connects to the websocket server, tries to reconnect if the connection is lost
		 */
		socket = new WebSocket(`ws://${window.location.host}/ws/queue/${roomName}/`);

		socket.onopen = handleSocketOpen;
		socket.onmessage = handleSocketMessage;
		socket.onerror = handleSocketError;
		socket.onclose = handleSocketClose;
	}

	function handleSocketOpen(event) {
		console.log('WebSocket is open now');
	}

	function handleSocketMessage(event) {
		/**
		 * When fist establish the connection with the websocket server it's gonna
		 * receive the queue size, after, it's gonna update the queue size with
		 * the data from the server
		 */
		const data = JSON.parse(event.data);

		try {
			if (data.hasOwnProperty('queueSize')) {
				handleQueue.handleDisplayQueue(data.queueSize, queueContainer);
			} else if (data.hasOwnProperty('hasTheQueueIncreased')) {
				if (data.hasTheQueueIncreased)
					handleQueue.handleIncreaseQueue(queueContainer);
				else
					handleQueue.handleDecreaseQueue(queueContainer);
			} else {
				throw 'A different property was given';
			}
		} catch(err) {
			console.error(err);
		}
	}

	function handleSocketError(event) {
		console.error(`WebSocket error observed: ${event}`);
	}
});