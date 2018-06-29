$(document).ready(function(){

  function start_long_task() {
      // add task status elements
      div = $('<div class="progress"><div></div><div>0%</div><div>...</div><div>&nbsp;</div></div><hr>');
      $('#progress').append(div);

      // send ajax POST request to start background job
      $.ajax({
          type: 'POST',
          url: '/longtask',
          data: JSON.stringify(usr_data, null, '\t'),
          contentType: 'application/json;charset=UTF-8',
          success: function(data, status, request) {
              status_url = request.getResponseHeader('Location');
              update_progress(status_url, nanobar, div[0]);
          },
          error: function() {
              alert('Unexpected error');
          }
      });
  }
  
};
