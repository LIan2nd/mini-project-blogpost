function createPost() {

  const title = $('#title').val();
  const body = $('#body').val();
  const author = $('#author').val();

  $.ajax({
    type: "POST",
    url: "/blog",
    data: { title, body, author },
    success: res => {
      if (res.result === "success") {
        alert(res.message);
        window.location.href = '/blog';
      } else {
        alert("Something Wrong");
      }
    }
  })
}

function editPost(id) {

  const title = $('#title').val();
  const body = $('#body').val();
  const author = $('#author').val();

  $.ajax({
    type: "PUT",
    url: `/blog/${id}`,
    data: { title, body, author },
    success: res => {
      if (res.result === "success") {
        alert(res.message);
        window.location.href = '/blog';
      } else {
        alert("Something Wrong");
      }
    }
  })
}

function deletePost(slug) {
  const deletePost = confirm("Are you sure, wanna delete this post?");
  if (deletePost) {
    $.ajax({
      type: "delete",
      url: `/blog/${slug}`,
      data: {},
      success: res => {
        if (res.result === 'success') {
          alert(res.message);
          location.reload();
        } else {
          alert("Something wrong!");
        }
      }
    })
  }
}