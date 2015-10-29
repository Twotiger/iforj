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


        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                function getCookie(name) {
                    var cookieValue = null;
                    if (document.cookie && document.cookie != '') {
                        var cookies = document.cookie.split(';');
                        for (var i = 0; i < cookies.length; i++) {
                            var cookie = jQuery.trim(cookies[i]);
                            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                                break;
                            }
                        }
                    }
                    return cookieValue;
                }
                if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                    xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                }
            }
        });