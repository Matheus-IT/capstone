let currentPage = 1;

document.addEventListener('DOMContentLoaded', function() {
	const feedbackSubmit = document.querySelector('.feedback-submit-content');
	const heightBefore = feedbackSubmit.style.height;

	const buttonLoadMoreFeedbacks = document.querySelector('.load-more-feedbacks');
	buttonLoadMoreFeedbacks.onclick = fetchMoreUserFeedbacks;

	feedbackSubmit.addEventListener('focus', function() {
		this.style.height = '24.2em';
	});

	feedbackSubmit.addEventListener('focusout', function() {
		this.style.height = heightBefore;
	});

	function fetchMoreUserFeedbacks() {
		let pageNumber = ++currentPage;

		fetch(`/more-user-feedback/${pageNumber}/`)
		.then(res => handleResponse(res))
		.then(data => {
			data.feedbacks.forEach(feedback => {
				const newPost = renderNewPost(feedback);

				const feedbackPosts = document.querySelector('.feedback__posts');
				feedbackPosts.append(newPost);
			});
		})
		.catch(err => {
			console.log(err);
		});
	}

	function handleResponse(res) {
		if (res.ok)
			return res.json();
		else if (res.status === 404)
			return Promise.reject('Error 404');
		else
			return Promise.reject(`Something doesn't seem right: ${res.status}`);
	}

	function renderNewPost(feedback) {
		const talkText = document.createElement('div');
		talkText.classList.add('talktext');
		talkText.innerHTML = feedback.content;

		const talkBuble = document.createElement('div');
		talkBuble.classList.add('talk-bubble');
		talkBuble.classList.add('tri-right');
		talkBuble.classList.add('left-in');
		talkBuble.append(talkText);

		const img = document.createElement('img');
		img.setAttribute('src', userImagePath);
		img.setAttribute('alt', 'user image');
		img.classList.add('user-photo');

		const post = document.createElement('div');
		post.classList.add('post');
		post.append(img);
		post.append(talkBuble)

		return post;
	}
});
