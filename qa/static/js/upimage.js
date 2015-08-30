        var uploader = Qiniu.uploader({
            runtimes: 'html5,flash,html4', 
            browse_button: 'pickfiles',
            uptoken_url: '/qntoken/',
            unique_names: true,
            domain: 'http://7xkozr.com1.z0.glb.clouddn.com/',
            container: 'container',  
            max_file_size: '4mb',     
            flash_swf_url: 'js/plupload/Moxie.swf',
            max_retries: 3,         
            dragdrop: true,          
            drop_element: 'container',
            chunk_size: '4mb',
            auto_start: true,
            init: {
                'FilesAdded': function(up, files) {
                    plupload.each(files, function(file) {
                    });
                },
                'BeforeUpload': function(up, file) {
                    console.log('ok')
                },
                'UploadProgress': function(up, file) {
                },
                'FileUploaded': function(up, file, info) {
                    var domain = up.getOption('domain');
                    var res = $.parseJSON(info);
                    var sourceLink = domain + res.key; 
                    editor.getElement('editor').body.innerHTML=editor.getElement('editor').body.innerHTML+'![Alt text]('+sourceLink+')'
                },
                'Error': function(up, err, errTip) {
                    alert('上传图片出现错误,检查系统时间,再次重新上传');
                },
                'UploadComplete': function() {
                },
                'Key': function(up, file) {
                    var key = "";
                    return key
                }
            }
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
