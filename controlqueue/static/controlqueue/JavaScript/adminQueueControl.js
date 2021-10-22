document.addEventListener('DOMContentLoaded', function() {
	const queueDomObject = document.querySelector('#displayQueueSize');
	let queueSize = 0;

	const buttonIncrease = document.querySelector('#increase');
	buttonIncrease.onclick = function() {
		communicateToWebsocketServer(queueSize + 1);
	}

	const buttonDecrease = document.querySelector('#decrease');
	buttonDecrease.onclick = function() {
		if (queueSize > 0)
			communicateToWebsocketServer(queueSize - 1);
	}

	let socket;
	socketClose();

	function socketOpen(event) {
		console.log('WebSocket connection open!');
	}

	function socketMessage(event) {
		/**
		 * When it first connects to the websocket server it's going to
		 * receive and update the queue size, after, it's gonna update the
		 * queue size
		 */
		const data = JSON.parse(event.data);

		try {
			if (data.hasOwnProperty('queueSize')) {
				queueSize = data.queueSize;
				updateQueueSize(data.queueSize, queueDomObject);
			} else if (data.hasOwnProperty('hasTheQueueIncreased')) {
				if (data.hasTheQueueIncreased)
					handleIncreaseQueueSize();
				else
					handleDecreaseQueueSize();
			} else {
				throw 'A different property was passed';
			}
		} catch(err) {
			console.error(err);
		}
	}

	function socketClose(event) {
		/**
		 * Connects to the server, such that when the connection is lost it tries
		 * to reconnect to the websocket server
		 */
		const roomName = document.querySelector('#room-name').innerHTML;
		const WEBSOCKET_QUEUE_URL = `ws://${window.location.host}/ws/queue/${roomName}/`;
		socket = new WebSocket(WEBSOCKET_QUEUE_URL);

		socket.onopen = socketOpen;
		socket.onmessage = socketMessage;
		socket.onclose = socketClose;
		socket.onerror = socketError;
	}

	function socketError(event) {
		console.log("WebSocket Error: " + JSON.stringify(event));
	}

	function handleIncreaseQueueSize() {
		queueSize++;
		updateQueueSize(queueSize, queueDomObject);
	}

	function handleDecreaseQueueSize() {
		if (queueSize > 0) {
			queueSize--;
			updateQueueSize(queueSize, queueDomObject);
		}
	}

	function updateQueueSize(newQueueSize, queueDomObj) {
		queueDomObj.innerHTML = newQueueSize;
	}

	function communicateToWebsocketServer(newQueueSize) {
		socket.send(JSON.stringify({
			queue_size: newQueueSize,
		}));
	}
});
