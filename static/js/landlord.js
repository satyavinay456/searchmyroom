
$("#landlord_add_btn").on('click',function(event) {
  event.preventDefault();

  $('#uploader').show();

  if ($("#property_category").val() == "categoryoption") {
    $('#uploader').hide();

    alert("please select category") //Focus on field
    return false;
  }


  if ($("input#property_name").val() == "") {
  $('#uploader').hide();
  $("input#property_name").focus(); //Focus on field
  return false;
  }

  if ($("input#total_rooms").val() == "" || !$.isNumeric($("input#total_rooms").val())) {
  $('#uploader').hide();
  $("input#total_rooms").focus(); //Focus on field
  return false;
  }

  if ($("input#available_rooms").val() == "" || !$.isNumeric($("input#available_rooms").val())) {
  $('#uploader').hide();
  $("input#available_rooms").focus(); //Focus on field
  return false;
  }


  if (Number($("input#available_rooms").val()) > Number($("input#total_rooms").val())) {
    alert('available_rooms should not be greater than total_rooms');

    $('#uploader').hide();
    return false;
  }


  if ($("input#average_rent").val() == "" || ! ($.isNumeric(Number($("input#average_rent").val())) && Math.floor(Number($("input#average_rent").val())) == Number($("input#average_rent").val()) )) {
    $('#uploader').hide();
    alert('please insert integer')
    $("input#average_rent").focus(); //Focus on field
    return false;
  }

  if (!$("input[name='optradio']:checked").val()) {
   alert('please select your Daily Breakfast');
   $('#uploader').hide();
   return false;
}

  var form_data = new FormData($('#upload_form')[0]);
  form_data.append('landlord_name',$('#landlord_name').text());
  form_data.append('landlord_email',$('#landlord_email').text());
  form_data.append('property_category',$('#property_category').val());
  form_data.append('property_name',$('#property_name').val());
  form_data.append('landlord_city',$('#select_city').val());
  form_data.append('landlord_state',$('#select_state').val());
  form_data.append('property_total_rooms',$('#total_rooms').val());
  form_data.append('property_available_rooms',$('#available_rooms').val());
  form_data.append('property_average_rent',Math.trunc($('#average_rent').val()));
  form_data.append('Daily_breakfast',$('input[name=optradio]:checked').val());
  var property_amenities = [];
  $(':checkbox:checked').each(function(i){
          property_amenities[i] = $(this).val();
  });

  //alert(property_amenities);
  form_data.append('property_amenities', property_amenities);


  $.ajax({
          url: "/add_property",
          data: form_data,
          type: 'POST',
          processData: false,  // tell jQuery not to process the data
          contentType: false ,
          success : function(response){
            $('#uploader').hide();
            if (response=="NOPHOTO"){
              alert("please upload photo");
              return false;
            }
            if (response.insert_status == 1) {
              $('#success_alert').show();
            } else {
              $('#danger_alert').show();
            }

            setTimeout(function () {
                     $('#success_alert').hide();
                     $('#danger_alert').hide();
                 },2000);
            setTimeout(function () {
              window.location.href="/landlord_properties";
            },2500);

          },
          error: function (request, status, error) {
                $('#uploader').hide();
                alert("please upload image and enter details correctly");
            }
    });

});
