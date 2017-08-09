;(function($, Common){
    
    function init(options) {
    }
    
    /*
    * input - search element id, result div id, ajax url, params
    * output - appends 10 results in the div
    */
    function bind_onkeyup(elem, resultelem, url, param) {
        $(elem).on('keyup', function(e) {
            var lis = '';
            $(resultelem).html(lis);

            if($.trim($(elem).val())) {
                var data = param + "=" + $.trim($(elem).val());
                var x = ajaxcall(url, 'GET', data);
            
                x.done(function(resp){
                    var response = resp.results;
                    $.each(response, function(i, e){
                        lis += '<a class="suggest_item" href="' + url + e.slug + '/">' + e.name + '</a>';
                    });
                    $(resultelem).html(lis);
                });
            }
        });
    }

    /*
    * make ajax call
    * input - url, method, param obj
    */
    function ajaxcall(url, method, param) {
        var response = $.ajax({
                        url:url,
                        method:method,
                        data:param,
                        beforeSend: function(xhr, settings) {
                            if (method=='POST' || method=='PUT') {
                                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                            }
                        }
                    });
        return response;
    }

    /*
    * onclick redirect to a url
    * input - elem, url, key, val_elem
    */
    function redirect(elem, url, key, val_elem) {
        $(elem).on('click', function(x) {
            var value = $.trim($(val_elem).val());
            if(value) {
                var href = url + "?" + key + "=" + value;
                window.location.href = href;
            }
        });
    }

    /*
    * returns true if get params exists in the current url
    */
    function is_param_exist() {
        if(document.URL.indexOf('?') != -1){
            return true;
        }
        return false;
    }

    /*
    * updates an existing queryparam or adds a new open
    * avoids same params to appear multiple times in the url 
    */
    function form_unique_params(key, data_elem, url=document.URL, sort=true) {
        var final_args = '';
        var args = url.split('?');
        if(sort) {
            var uniq = key + "=" + $(data_elem).data('order') + $(data_elem).data('key');
        } else {
            var uniq = key + "=" + data_elem;
        }
        if(args.length > 1) {
            $.each(args[1].split('&'), function(i, each) {
                if(each.indexOf(key) == -1) {
                    final_args += each + '&';
                }
            });
        }
        return args[0] + '?' + final_args + uniq
    }

    function verify_mandatory(obj, elem, error_message) {
        var error = 0;
        $.each(obj, function(key, val){
            // if any value blank, return false
            if($.trim(val) == '' ) {
                error += 1;
                $(elem).html(error_message);
                $(".alert_message_error").show();
            }

            // if mobile in key then, value should be integer and 10 digit long
            if(key.indexOf('mobile') != -1) {
                if(val.length != 10 || !$.isNumeric(val)) {
                    error += 1;
                    $(elem).html(Common.mobile_mandatory);
                }
            }
        });
        if(error==0) {
            return true;
        } else {
            return false;
        }
    }

    /*
    */
    function forceregister(user, action, isajax=true) {
        // show registration/login form
        // on successful registration/login, call action if isajax=true
        // hide registration form
        // hide requirement application form
        // show message returned by ajaxcall
    }


    // using jQuery
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    function show_alert(message) {
        $('html,body').animate({
            scrollTop: (0)},
            'slow');
        $("#alert_message").html(
            message + '<button class="btn-close" id="alert-close"><i class="fa fa-times" aria-hidden="true"></i></button>'
        ).fadeIn().fadeOut(20000, function() {
        });
        
        // alert close binding
        $("#alert-close").on('click', function() {
            $("#alert_message").hide()
        });
    }
    // list all urls to be used, whether ajax or redirect url
    Common.login_url = "/login/";
    Common.register_url = "/create-user/";
    Common.forgot_password_url = "/forgot-password/";
    Common.check_useravailable = "/user-exists/";


    // list of all messages
    Common.mandatory_params = "Error: Mandatory parameters missing";
    Common.mobile_mandatory = "Error: Mobile number should be 10 digit integer";
    Common.forgot_password_message = "Error: Please enter username";

    Common.init = init;
    Common.forceregister = forceregister;
    Common.bind_onkeyup = bind_onkeyup;
    Common.redirect = redirect;
    Common.ajaxcall = ajaxcall;
    Common.is_param_exist = is_param_exist;
    Common.form_unique_params = form_unique_params;
    Common.verify_mandatory = verify_mandatory;
    Common.show_alert = show_alert;

})($,(window.Common = window.Common || {}));
