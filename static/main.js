$(document).ready(function(){

  $("#retryBtn").hide();
  $("#alertDiv").hide();
  $("#loadingBtn").hide();

  $('.selectpicker').selectpicker();
  $('.selectpicker').selectpicker('val', ['TEXT', 'SOUND', 'IMAGE', 'VIDEO']);


  // SEND FORM

  $("#taskButton").click(function(e) {

    $("#alertDiv").hide();

    usr_data = {
            'key': $("#key").val(),
            'creator': $("#creator").val(),
            'type': $("#type").val(),
            'keywords': $("#keywords").val(),
            'from': $("#from").val(),
            'to': $("#to").val(),
            'places': $("#place").val()
            }

    // send ajax POST request to start background job
    $.ajax({
        type: 'POST',
        url: '/runTask',
        data: JSON.stringify(usr_data, null, '\t'),
        contentType: 'application/json;charset=UTF-8',
        success: function(data, status, request) {
            $("#loadingBtn").show();
            $("#taskForm").hide();
            status_url = request.getResponseHeader('Location');
            update_progress(status_url);
        },
        error: function() {
            alert('Unexpected error');
        }
    });
    e.preventDefault();
  });


  $("#retryBtn").click(function(e) {

    $("#alertDiv").hide();

    usr_data = {
            'key': $("#key").val(),
            'creator': $("#creator").val(),
            'date': $("#key").val(),
            'items_type': $("#items_type").val(),
            'items_dataProvider': $("#items_dataProvider").val(),
            'keywords': $("#keywords").val(),
            'from': $("#from").val(),
            'to': $("#to").val(),
            }

    // send ajax POST request to start background job
    $.ajax({
        type: 'POST',
        url: '/runTask',
        data: JSON.stringify(usr_data, null, '\t'),
        contentType: 'application/json;charset=UTF-8',
        success: function(data, status, request) {
            $("#retryBtn").hide();
            $("#taskForm").hide();
            $("#loadingBtn").show();
            status_url = request.getResponseHeader('Location');
            update_progress(status_url);
        },
        error: function() {
            alert('Unexpected error');
        }
    });
    e.preventDefault();
  });

  //retryBtn = '<a class="cust" href="/">Recommencer</a>';
  retryBtn = '<button class="cust" type="button" id="retryBtn">Recommencer</button>';
  form = '<button class="cust" type="button" id="taskButton">Task</button>';




  function update_progress(status_url) {

      // send GET request to status URL
      $.getJSON(status_url, function(data) {

        console.log(data.state);
        console.log(data);

          if (data['state'] == 'working') {
            // rerun in 2 seconds
            setTimeout(function() {
                update_progress(status_url);
            }, 2000);
          }
          else if (data['state'] == 'empty') {
            $("#taskForm").hide();
            $("#loadingBtn").show();
            $("#retryBtn").show();

            alert = '<div class="alert alert-success">Aucun élément ne correspond à votre requête...</div><br/>';
            $("#alertDiv").show();
            $("#loadingBtn").hide();
            $("#alertDiv").html(alert);

            setTimeout(function() {
                delayed_dir_cleaning(data['dir']);
            }, 500000);
          }
          else if (data['state'] == 'error') {
            alert = '<div class="alert alert-success"><strong>Une erreur est survenue : </strong>' + data.error + "</div>";
            $("#taskForm").hide();
            $("#loadingBtn").hide();
            $("#alertDiv").html(alert)
            $("#alertDiv").show();
            $("#retryBtn").show();

            setTimeout(function() {
                delayed_dir_cleaning(data['dir']);
            }, 500000);
          }
          else if (data['state'] == 'loaded') {
            u = '/display/' + data['dir'];
            location.replace(u);
            setTimeout(function() {
                delayed_dir_cleaning(data['dir']);
            }, 500000);
          }

      });
  };

});
