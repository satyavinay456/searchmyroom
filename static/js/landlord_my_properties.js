$('#select_state').on('click',function(){
  $('#uploader').show();
      $.ajax({
              url: "/getcities",
              data : { 'selected_state': $('#select_state').val()} ,
              type: 'POST',
              success : function(response){
                $('#uploader').hide();
                $('#select_city').html(response.cities)
              },
                        error: function (request, status, error) {
                            $('#uploader').hide();
                            alert("INTERNAL SERVER ERROR");
                            console.log(request.responseText);
                        }
        });
});
