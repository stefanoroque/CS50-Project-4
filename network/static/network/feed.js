// Wait for the DOM to be completely loaded before adding event listeners
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.like_unlike_btn').forEach(item => {
        item.addEventListener('click', event => {
          like_unlike(item.id)
        })
      })
  });

// Function to like or unlike a post
function like_unlike(post_id) {
  // Create JSON
    fetch('/like_unlike', {
    method: 'POST',
    body: JSON.stringify({
        post_id: post_id
    })
  })
  // Put response into json form
  .then(response => response.json())
  .then(result => {
    if (result.message == "post liked successfully") {
      // Post has been liked successfully
      console.log(result);
      // TODO: Update HTML to reflect the like
      let old_num_likes = document.getElementById(post_id+"_numlikes").innerHTML;
      document.getElementById(post_id+"_numlikes").innerHTML = parseInt(old_num_likes) + 1

    } else {
      // Post has been unliked successfully
      console.log(result);
      // TODO: Update HTML to reflect the unlike
      let old_num_likes = document.getElementById(post_id+"_numlikes").innerHTML;
      document.getElementById(post_id+"_numlikes").innerHTML = parseInt(old_num_likes) - 1
    } 
  })
  .catch(error => {
    console.log('Error:', error)
  });

  // Stop form from submitting
  return false;
}