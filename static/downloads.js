$(document).ready(function(){

  $("#csvBtn").click(function(e) {
    u = '/result' + ;
    $.ajax({
      type: "POST",
      url: u
  })

}
