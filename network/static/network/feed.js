// Wait for the DOM to be completely loaded before adding event listeners
document.addEventListener('DOMContentLoaded', function() {
  var el = document.getElementById('follow_unfollow_btn');
  if(el){
    el.addEventListener('click', () => follow_unfollow());
  }

  document.querySelectorAll('.like_unlike_btn').forEach(item => {
      item.addEventListener('click', event => {
        like_unlike(item.id)
      })
    })
  });

// Function to follow or unfollow a user
function follow_unfollow() {
  // I think that getting the username like this has security vulnerabilities, if you change the innerHTML with "inspect", you can change how the JS function runs
  var username = document.getElementById("desired_username").innerHTML
  // Create JSON
  fetch('/follow_unfollow', {
    method: 'POST',
    body: JSON.stringify({
        desired_username: username
    })
  })
  // Put response into json form
  .then(response => response.json())
  .then(result => {
    if (result.message == "user followed successfully") {
      // User has been followed successfully
      console.log(result);
      // TODO: Update HTML to reflect the follow
      var old_num_followers = document.getElementById("num_followers").innerHTML.replace('Followers: ','');
      console.log(parseInt(old_num_followers));
      document.getElementById("num_followers").innerHTML = 'Followers: ' + (parseInt(old_num_followers) + 1);
      // Change button to unfollow
      document.getElementById("follow_unfollow_btn").className = "btn btn-outline-primary";
      document.getElementById("follow_unfollow_btn").innerHTML = "Unfollow"
      
    } else {
      // User has been unfollowed successfully
      console.log(result);
      // Update HTML to reflect the unfollow
      var old_num_followers = document.getElementById("num_followers").innerHTML.replace('Followers: ','');
      console.log(parseInt(old_num_followers));
      document.getElementById("num_followers").innerHTML = 'Followers: ' + (parseInt(old_num_followers) - 1);
      // Change button to follow
      document.getElementById("follow_unfollow_btn").className = "btn btn-primary";
      document.getElementById("follow_unfollow_btn").innerHTML = "Follow"

    } 
  })
  .catch(error => {
    console.log('Error:', error)
  });

  // Stop form from submitting
  return false;
}

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
      // Update HTML to reflect the like
      let old_num_likes = document.getElementById(post_id+"_numlikes").innerHTML;
      document.getElementById(post_id+"_numlikes").innerHTML = parseInt(old_num_likes) + 1;

    } else {
      // Post has been unliked successfully
      console.log(result);
      // Update HTML to reflect the unlike
      let old_num_likes = document.getElementById(post_id+"_numlikes").innerHTML;
      document.getElementById(post_id+"_numlikes").innerHTML = parseInt(old_num_likes) - 1;
    } 
  })
  .catch(error => {
    console.log('Error:', error);
  });

  // Stop form from submitting
  return false;
}

// Function to edit a post
function edit_post(post_id) {
  var edit_box = document.querySelector(`#edit_box_${post_id}`);
  var post_content = document.querySelector(`#post_content_${post_id}`);

  // Reset the text in the text area to the original post content
  edit_box.value = post_content.innerHTML;
  edit_box.style.display = 'block';
  document.querySelector(`#edit_btn_${post_id}`).style.display = 'block';
  document.querySelector(`#cancel_btn_${post_id}`).style.display = 'block';
  post_content.style.display = 'none';
}

function cancel_edit_post(post_id) {
  document.querySelector(`#edit_box_${post_id}`).style.display = 'none';
  document.querySelector(`#edit_btn_${post_id}`).style.display = 'none';
  document.querySelector(`#cancel_btn_${post_id}`).style.display = 'none';
  document.querySelector(`#post_content_${post_id}`).style.display = 'block';
}

function save_edit_post(post_id) {
    // Create JSON
    fetch('/edit_post', {
      method: 'PUT',
      body: JSON.stringify({
          post_id: post_id,
          new_content: document.querySelector(`#edit_box_${post_id}`).value
      })
    })
    // Put response into json form
    .then(response => response.json())
    .then(result => {
      if (result.message == "post edited successfully") {
        console.log(result);
        document.querySelector(`#post_content_${post_id}`).innerHTML = document.querySelector(`#edit_box_${post_id}`).value
        document.querySelector(`#edit_box_${post_id}`).style.display = 'none';
        document.querySelector(`#edit_btn_${post_id}`).style.display = 'none';
        document.querySelector(`#cancel_btn_${post_id}`).style.display = 'none';
        document.querySelector(`#post_content_${post_id}`).style.display = 'block';
      } else {
        console.log('failure')
      } 
    })
    .catch(error => {
      console.log('Error:', error)
    });
}