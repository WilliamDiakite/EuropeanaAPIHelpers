$(document).ready(function(){

  $("#retryBtn").hide();

  // USEFUL STUFF

  retryBtn = '<a class="cust" href="/">Recommencer</a>';
  form = '<button class="cust" type="button" id="taskButton">Task</button>';


  // SEND FORM

  $("#taskButton").click(function(e) {

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

    $.ajax({
          type: "POST",
          url:'/runTask',
          data: JSON.stringify(usr_data, null, '\t'),
          contentType: 'application/json;charset=UTF-8',
     });
    e.preventDefault();
  });



  // WAIT FOR JOB TO BE DONE

  var namespace='/long_task';
  var socket = io.connect('http://' + document.domain + ':' + location.port+namespace);

  socket.on('connect', function() {
    socket.emit('join_room');
  });

  socket.on('working', function() {
    $("#taskForm").empty();
    $("#taskForm").html('<button class="cust"><i class="fa fa-circle-o-notch fa-spin"></i>  Récupération...</button>');
  });

  socket.on('error', function(data) {

    alert = '<div class="alert alert-success"><strong>Une erreur est survenue : </strong>' + data.msg + "</div>";
    $("#taskForm").html(alert);
    $("#taskForm").prepend(retryBtn);

    $.ajax({type: "POST",
          url: '/result',
          data: JSON.stringify('error', null, '\t'),
          contentType: 'application/json;charset=UTF-8',
    });
  });


  socket.on('empty', function() {
    alert = '<div class="alert alert-success">Aucun élément ne correspond à votre requête...</div><br/>';
    $("#taskForm").empty();
    $("#taskForm").html(alert);
    $("#taskForm").prepend(retryBtn);

    $.ajax({type: "POST",
          url: '/result',
          data: JSON.stringify('empty', null, '\t'),
          contentType: 'application/json;charset=UTF-8',
    });
  });

  socket.on('done', function(data) {
    result = data.msg;
    console.log('this is the entire data');
    console.log(result);

    console.log('ELEMENTS PRESENTS');
    $("#taskForm").empty();

    displ_url = '/display/' + result.dir;
    $("#taskForm").html('<a class="cust" href="' + displ_url + '"><h4>Results</h4></a>');

  });
});
