let post_like_id = -1;
let post_edit_id = -1;

document.addEventListener('DOMContentLoaded', function () {
  
  //Ajax function to manage Like
  $(document).on('submit','#like-dislike-form',function(e){
    wait(400);
    console.log("multiple excecution? " + post_like_id);
    e.preventDefault();
    var like_dislike_btn = $("#btn_like_" + post_like_id).val();
  
    $.ajax({
        type:'POST',
        url:'',
        data:
        {
            btn_like_dislike:like_dislike_btn,
            id_post:post_like_id,
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
        },
        success: function(response) {
          console.log("success call :)");
          successCallback(response, post_like_id);
        }
    });
  });

  //Ajax function to manage edit the post's content
  $(document).on('submit','#edit-form',function(e){
    e.preventDefault();
    var edit_button = $("#btn_edit_post").val();
    var text_area = $("#text_area_post_" + post_edit_id).val();
    var message = "";
    if(text_area == "") {
        message = "Oops, the content must not be empty!";
    }
    else {
        message = "Post updated!";
    }
    
    $.ajax({
        type:'POST',
        url:'',
        data:
        {
            edit_post:edit_button,
            text_area_edit_post:text_area,
            id_post:post_edit_id,
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
        },
        success:function(){
              alert(message);
                }
        })
    });
});

function edit_post(post_id) {
  const id_p_content = 'content_post_' + post_id;
  const id_text_a = 'text_area_post_' + post_id;
  const id_btn_save = 'btn_save_post_' + post_id;
  const id_btn_cancel = 'btn_cancel_edit_' + post_id;
  document.querySelector('#' + id_p_content).style.display = 'none';
  document.querySelector('#' + id_text_a).classList.replace('text_area_hidden', 'text_area_visible');
  document.querySelector('#' + id_btn_save).classList.replace('btn_hidden', 'btn_visible');
  document.querySelector('#' + id_btn_cancel).classList.replace('btn_hidden', 'btn_visible');
}

function save_post(post_id) {
  post_edit_id = post_id;
  const id_text_a = 'text_area_post_' + post_id;
  const id_p_content = 'content_post_' + post_id;
  const id_btn_save = 'btn_save_post_' + post_id;
  const id_btn_cancel = 'btn_cancel_edit_' + post_id;
  const text_area = document.querySelector("#" + id_text_a);
  const p_content = document.querySelector("#" + id_p_content);
  const btn_save = document.querySelector("#" + id_btn_save);
  const btn_cancel = document.querySelector("#" + id_btn_cancel);
  const value_text_area = text_area.value;

  if(value_text_area != "") {
    p_content.innerHTML=value_text_area;
    text_area.classList.replace('text_area_visible', 'text_area_hidden');
    btn_save.classList.replace('btn_visible', 'btn_hidden');
    btn_cancel.classList.replace('btn_visible', 'btn_hidden');
    p_content.style.display = 'block';
  }
}

function cancel_edit(post_id) {
  const id_text_a = 'text_area_post_' + post_id;
  const id_p_content = 'content_post_' + post_id;
  const id_btn_save = 'btn_save_post_' + post_id;
  const id_btn_cancel = 'btn_cancel_edit_' + post_id;
  const text_area = document.querySelector("#" + id_text_a);
  const p_content = document.querySelector("#" + id_p_content);
  const btn_save = document.querySelector("#" + id_btn_save);
  const btn_cancel = document.querySelector("#" + id_btn_cancel);
  
  p_content.style.display = 'block';
  text_area.classList.replace('text_area_visible', 'text_area_hidden');
  btn_save.classList.replace('btn_visible', 'btn_hidden');
  btn_cancel.classList.replace('btn_visible', 'btn_hidden');
}

function like_dislike(post_id) {
  console.log("Arrives to like - dislike function " + post_id);
  post_like_id = post_id;
}

function successCallback(responseObj, post_id){
  const id_like_counter = 'like_counter_' + post_id;
  const like_counter = document.querySelector("#" + id_like_counter);
  var value_like_counter = parseInt(like_counter.innerHTML);
  //var value_like_counter = like_counter.value;
  //get value in front does not work, call a back function to get the value by Ajax Async
  
  console.log("Like counter: " + like_counter.innerHTML);

  if(JSON.stringify(responseObj) == '{"flag":"like"}')
  {
    value_like_counter = value_like_counter + 1;
    like_counter.innerHTML = value_like_counter;
  }
  else if(JSON.stringify(responseObj) == '{"flag":"dislike"}')
  {
    value_like_counter = value_like_counter - 1;
    like_counter.innerHTML = value_like_counter;
  }
  console.log("value: " + JSON.stringify(responseObj));
}

// Support functions

function wait(ms) {
  var start = new Date().getTime();
  var end = start;
  while (end < start + ms) {
    end = new Date().getTime();
  }
}