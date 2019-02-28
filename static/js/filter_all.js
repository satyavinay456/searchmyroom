$('#filter_all').on('click',function(){
  if ($('input[name="bf_radio"]:checked').length == 0) {
         alert('select');
         return false; }
         
      var selectedValues = [];
         $('select.' + 'selectpicker').children('option:selected').each( function() {
              var $this = $(this);
              selectedValues.push($this.text());
      });


      $('#tenant_uploader').show();
      $.ajax({
              url: "/filter_all",
              data : { 'location': $('#available_states').val() , 'rooms_available' : $('input[name=roomradio]:checked').val(), 'amenities_list':selectedValues, 'breakfast_condition':$('input[name=bf_radio]:checked').val() } ,
              type: 'POST',
              success : function(response){
                 $('#tenant_uploader').hide();
                 $('#cards_row').html(response)

              },
                error: function (request, status, error) {
                    $('#tenant_uploader').hide();
                    alert("SERVER ERROR");
                }
        });
});
