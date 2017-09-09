;(function($, Common, MyProfile){

    function init(options){
        Common.bind_key_escape();
        MyProfile.bind_key_enter();
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
        bind_save_basic_info()
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
                $(".alert_message_error").show(1000);
                if(resp.status==true){
                    Common.after_login_process(resp);
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
                    $(".alert_message_error").show(1000);
                    if(resp.status==true){
                        // on reset password, set new password to mobile and just click on sign-in
                        $(".tabs-login label").first().trigger('click');
                        $("#login_message").html(resp.message);
                        $(".alert_message_error").show(1000);
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
                'user_role':$("#user_role").val()
            }
            var verify = Common.verify_mandatory(credentials, '#register_message', Common.mandatory_params);
            if(!verify) {
                return false;
            }
            x = Common.ajaxcall(Common.register_url, 'POST', credentials);
            x.done(function(resp) {
                $("#register_message").html(resp.message);
                $(".alert_message_error").show(1000);
                if(resp.status==true){
                    Common.after_login_process(resp);
                }
            });
        });
    }


    function bind_key_enter() {
        $(document).keyup(function(e) {
            if (e.keyCode == 13) { // Enter key maps to keycode `13`
                var action_buttons = $(".btn-login");
                if(action_buttons.length > 0) {
                    $.each(action_buttons, function(k, v) {
                        // TODO Submit login/register/reset whichever is displayed
                        /*if(v.css("display", "block")) {
                            try { v.click(); }
                            catch(err) {}
                        }*/
                    });
                }
            }
        });
    }

    function bind_save_basic_info() {
        $('#basic_info_save').on('click', function() {
            // form all input values dict and save it using ajax
            var values = {};
            $.each($('#profileform').serializeArray(), function(i, field) {
                values[field.name] = field.value;
            });

            $("#profileform").attr("action", "?alert_message=Profile updates successfully.");
            $("#profileform").submit();
            /*x = Common.ajaxcall(Common.update_profile, 'POST', values);
            x.done(function(resp) {
                if(resp.status==true) {
                    Common.show_alert(resp.message)
                }
                else {
                    Common.show_alert(resp.message)
                }
            });*/
        });
    }

    MyProfile.init = init;
    MyProfile.bind_login = bind_login;
    MyProfile.bind_registration = bind_registration;
    MyProfile.bind_key_enter = bind_key_enter;
    MyProfile.bind_save_basic_info = bind_save_basic_info;

})($, Common, window.MyProfile= window.MyProfile || {})
