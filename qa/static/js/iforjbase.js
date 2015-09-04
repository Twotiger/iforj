/**
 * Created by twotiger on 2015/8/30.
 */


  $("#log_but").click(function() {
            var email =$("#email").val();
            var password = $('#password').val();

            $.ajax({
                type:'POST',
                url:'/login/',
                data:{"email":email,"password":password},
                dataType:'json',
                success:function(){
                    window.location.reload();
                },
                error:function(msg){
                    alert(msg.responseText)
                }
            });
            // alert(theContent)
        });