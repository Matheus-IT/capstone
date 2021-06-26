document.addEventListener('DOMContentLoaded', function() {
    const feedbackSubmit = document.querySelector('.feedback-submit-content');
    const heightBefore = feedbackSubmit.style.height;

    feedbackSubmit.addEventListener('focus',function() {
        this.style.height = '24.2em';
    });

    feedbackSubmit.addEventListener('focusout',function() {
        this.style.height = heightBefore;
    });
});