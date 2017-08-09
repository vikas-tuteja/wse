;(function($, Common, MyProfile){

    function init(options){
        // js for my profile page events link -- starts
        // default show only first div content and thus bg -select only first label
        $('div[id^="content-"]').css("display","none");

        $("#content-1").css("display","block");
        $("#label-1").addClass("bg-selected");


        // onclick label, show its respective content
        $('div[id^="label-"]').on('click', function() {
            $('div[id^="label-"]').removeClass("bg-selected");
            $(this).addClass("bg-selected");

            $('div[id^="content-"]').css("display","none");
            $('#content-'+$(this).data('num')).css("display","block");
        });
        // js for my profile page events link -- ends

        bind_login("#login");
        bind_forgot_password("#forgot_password");
        bind_registration("#register");
        bind_checkavailibility("#reg_username");
    }
    
    function bind_checkavailibility(elem) {
        $(elem).on('blur', function() {
            var username = $(elem).val();
            if(username){
                // check redis user exists
                x = Common.ajaxcall(Common.check_useravailable, 'GET', {'username':username});
                // if not avialble, change username alert
                x.done(function(resp) {
                    if(resp.status==true) {
                        $("#register_message").html(resp.message);
                        $(".alert_message_error").show(1000);
                    }
                    else {
                        $(".alert_message_error").hide(1000);
                    }
                });
            }
        });
    }
    
    function bind_login(elem) {
        $(elem).on('click', function() {
            var credentials = {
                'username':$("#username").val(),
                'password':$("#password").val()
            }
            var verify = Common.verify_mandatory(credentials, '#login_message', Common.mandatory_params);
            if(!verify) {
                return false;
            }
            x = Common.ajaxcall(Common.login_url, 'GET', credentials);
            x.done(function(resp) {
                $("#login_message").html(resp.message);
                if(resp.status==true){
                    $(".btn-close").trigger("click");
                    var url = document.URL
                    // if last character #, remove it
                    if(url[url.length-1] == "#") {
                        url = url.slice(0,-1)
                    }
                    url = Common.form_unique_params('alert_message', resp.message, url, false);
                    window.location.href = url;
                }
            });
        });
    }

    function bind_forgot_password(elem) {
        $(elem).on('click', function() {
            var credentials = {
                'username':$("#fp_username").val(),
            }
            var verify = Common.verify_mandatory(credentials, '#forgot_password_message', Common.forgot_password_message);
            if(!verify) {
                return false;
            }
            else {
                x = Common.ajaxcall(Common.forgot_password_url, 'PUT', credentials);
                x.done(function(resp) {
                    $("#forgot_password_message").html(resp.message);
                    if(resp.status==true){
                        $(".btn-close").trigger("click");
                        // TODO change sign in icon to user profile icon 
                    }
                });
            }
        });
    }

    function bind_registration(elem) {
        $(elem).on('click', function() {
            var credentials = {
                'username':$("#reg_username").val(),
                'mobile':$("#reg_mobile").val(),
                'password':$("#reg_password").val(),
                'confirm_password':$("#reg_confirm_password").val(),
                // default user role is candidate
                'user_role':'candidate'
            }
            var verify = Common.verify_mandatory(credentials, '#register_message', Common.mandatory_params);
            if(!verify) {
                return false;
            }
            x = Common.ajaxcall(Common.register_url, 'POST', credentials);
            x.done(function(resp) {
                $("#register_message").html(resp.message);
                if(resp.status==true){
                    $(".btn-close").trigger("click");
                    // TODO change sign in icon to user profile icon 
                }
            });
        });
    }


    MyProfile.init = init;
    MyProfile.bind_login = bind_login;
    MyProfile.bind_registration = bind_registration;

})($, Common, window.MyProfile= window.MyProfile || {})
