// Wait for the DOM to be completely loaded before adding event listeners
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.like_unlike_btn').forEach(item => {
        item.addEventListener('click', event => {
          console.log(item.id)
        })
      })
  });

