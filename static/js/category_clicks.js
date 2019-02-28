$("#Apartments_btn").on('click',function(event) {
  $('#tenant_uploader').show();
  $.ajax({
          url: "/category_clicks",
          data: {"name":"Apartments"},
          type: 'POST',
          success : function(response){
            $('#tenant_uploader').hide();
            $('#cards_row').html(response.cards_html)
          },
            error: function (request, status, error) {
                $('#tenant_uploader').hide();
                alert(request.responseText);
            }
    });
  });
  $("#Resort_btn").on('click',function(event) {
    $('#tenant_uploader').show();
    $.ajax({
            url: "/category_clicks",
            data: {"name":"Resort"},
            type: 'POST',
            success : function(response){
              $('#tenant_uploader').hide();
              $('#cards_row').html(response.cards_html)

            },
              error: function (request, status, error) {
                  $('#tenant_uploader').hide();
                  alert(request.responseText);
              }
      });
    });
    $("#Villas_btn").on('click',function(event) {
      $('#tenant_uploader').show();
      $.ajax({
              url: "/category_clicks",
              data: {"name":"Villas"},
              type: 'POST',
              success : function(response){
                $('#tenant_uploader').hide();
                $('#cards_row').html(response.cards_html)

              },
                error: function (request, status, error) {
                    $('#tenant_uploader').hide();
                    alert(request.responseText);
                }
        });
      });


      $("#Cabins_btn").on('click',function(event) {
        $('#tenant_uploader').show();
        $.ajax({
                url: "/category_clicks",
                data: {"name":"Cabins"},
                type: 'POST',
                success : function(response){
                  $('#tenant_uploader').hide();
                  $('#cards_row').html(response.cards_html)

                },
                  error: function (request, status, error) {
                      $('#tenant_uploader').hide();
                      alert(request.responseText);
                  }
          });
        });

        $("#Cottage_btn").on('click',function(event) {
          $('#tenant_uploader').show();
          $.ajax({
                  url: "/category_clicks",
                  data: {"name":"Cottage"},
                  type: 'POST',
                  success : function(response){
                    $('#tenant_uploader').hide();
                    //alert(response)
                    //$('#Apartments_btn_val').text(response)
                    $('#cards_row').html(response.cards_html)

                  },
                    error: function (request, status, error) {
                        $('#tenant_uploader').hide();
                        alert(request.responseText);
                    }
            });
          });

          $("#show_all_btn").on('click',function(event) {
            window.location.href="/tenant"
            });

            $("#sort_selected").on('change',function(event) {
              console.log($('#sort_selected').val());
              if ($('#sort_selected').val()=='sort') {
                return
              }
              $('#tenant_uploader').show();
              $.ajax({
                      url: "/category_clicks",
                      data: {"name":$('#sort_selected').val()},
                      type: 'POST',
                      success : function(response){
                        $('#tenant_uploader').hide();
                        $('#cards_row').html(response.cards_html)

                      },
                        error: function (request, status, error) {
                            $('#tenant_uploader').hide();
                            alert(request.responseText);
                        }
                });
              });
