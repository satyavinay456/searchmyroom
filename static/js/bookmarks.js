// $('#cards_row #main_card img').on('click',function(){
//   var id='#'+$(this).attr('class')
//   // alert(id);
//        $(id).hide();
//       $.ajax({
//               url: "/bookmarks_process",
//               data : { 'imageurl': $(this).attr('class') } ,
//               type: 'POST',
//               success : function(response){
//                  // alert(response);
//                 if (response=="by_success"){
//                   $(id+"ed").show();
//                 }
//                 if (response=="bn_success"){
//                   id=id.substring(0, id.length - 2);
//                   // alert(id)
//                   $(id).show()
//                 }
//               },
//                         error: function (request, status, error) {
//                           $(id).show();
//
//                             alert("cant bookmark");
//                         }
//         });
// });


$('body #mkdiv #cards_row').on('click','#main_card .card-body img',function(){
   var id='.'+$(this).attr('class')
  // alert(id);
       // $("body #mkdiv #cards_row #main_card .card-body "+id).hide();
       $('#main_card .card-body '+id).hide();
      $.ajax({
              url: "/bookmarks_process",
              data : { 'imageurl': $(this).attr('class') } ,
              type: 'POST',
              success : function(response){
                //  alert(response);

                if (response=="by_success"){
                  $("#main_card .card-body "+id+"ed").show();
                }
                if (response=="bn_success"){
                  id=id.substring(0, id.length - 2);
                  // alert(id)
                  $(id).show()
                }
              },
                        error: function (request, status, error) {
                          $(id).show();

                            alert("cant bookmark");
                        }
        });
});

$('#cards_row #main_card #more_info').on('click',function(){
  var id=$(this).attr('unique')
    window.location.href="/property/"+id
  });
