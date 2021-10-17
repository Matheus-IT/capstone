let currentPage = 1;

document.addEventListener("DOMContentLoaded", function () {
  // ----------------------- Handle animation of text area -------------------
  const feedbackSubmit = document.querySelector("#feedback-content");
  const heightBefore = feedbackSubmit.style.height;
  feedbackSubmit.addEventListener("focus", function () {
    this.style.height = "24.2em";
  });
  feedbackSubmit.addEventListener("focusout", function () {
    this.style.height = heightBefore;
  });
  // -------------------------------------------------------------------------

  const feedbackForm = document.querySelector("#submit-feedback-form");
  feedbackForm.addEventListener("submit", handleSubmitFeedback);

  const buttonLoadMoreFeedbacks = document.querySelector(
    ".load-more-feedbacks"
  );
  buttonLoadMoreFeedbacks.onclick = fetchMoreUserFeedbacks;

  function handleSubmitFeedback(event) {
    event.preventDefault();

    const contentFormField = document.querySelector("#feedback-content");

    fetch("/submit-new-feedback/", {
      method: "POST",
      body: JSON.stringify({
        content: contentFormField.value,
      }),
      headers: {
        "X-CSRFToken": getCookie("csrftoken"),
        "X-Requested-With": "XMLHttpRequest", //Necessary to work with request.is_ajax()
      },
    })
      .then((response) => response.json())
      .then((data) => {
        const feedback = data.feedback;
        const feedbackPosts = document.querySelector("#feedback-posts");
        feedbackPosts.prepend(renderNewPost(feedback));
      })
      .catch((error) => {
        console.log(`Something went wrong: ${error}`);
      });
  }

  function fetchMoreUserFeedbacks() {
    let pageNumber = ++currentPage;

    fetch(`/more-user-feedback/${pageNumber}/`)
      .then((res) => handleResponse(res))
      .then((data) => {
        data.feedbacks.forEach((feedback) => {
          const newPost = renderNewPost(feedback);

          const feedbackPosts = document.querySelector("#feedback-posts");
          feedbackPosts.append(newPost);
        });
      })
      .catch((err) => {
        console.log(err);
      });
  }

  function handleResponse(res) {
    if (res.ok) return res.json();
    else if (res.status === 404) return Promise.reject("Error 404");
    else return Promise.reject(`Something doesn't seem right: ${res.status}`);
  }

  function renderNewPost(feedback) {
    const content = document.createElement("p");
    content.classList.add("content");
    content.innerHTML = feedback.content;

    const talkText = document.createElement("div");
    talkText.classList.add("talktext");
    talkText.append(content);

    const talkBuble = document.createElement("div");
    talkBuble.classList.add("talk-bubble");
    talkBuble.classList.add("tri-right");
    talkBuble.classList.add("left-in");
    talkBuble.append(talkText);

    const img = document.createElement("img");
    img.setAttribute("src", userImagePath);
    img.setAttribute("alt", "user image");
    img.classList.add("user-photo");

    const post = document.createElement("div");
    post.classList.add("post");
    post.append(img);
    post.append(talkBuble);

    return post;
  }
});

function getCookie(name) {
  if (document.cookie && document.cookie !== "") {
    var cookies = document.cookie.split(";");

    for (let i = 0; i < cookies.length; i++) {
      let cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === name + "=") {
        var cookieValue = null;
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
