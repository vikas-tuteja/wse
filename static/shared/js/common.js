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
        // if login -> call action
        if(user) {
            window.location.href = action;
        }
        else {
            // show registration/login form if not logged in
            $(".sign-in").trigger('click');
            $("#action").val(action);
        }
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

    function convert_queryparams_to_object(string) {
        try {
            return JSON.parse('{"' + decodeURI(string.replace(/&/g, "\",\"").replace(/=/g,"\":\"")) + '"}')
        } catch(err) {
            return {}
        }
    }
    /*
    * remove alert message from get params and return the new url
    */
    function remove_alert_message(url) {
        var link = url.split('?');
        // if no parameters, return only url
        if(link.length == 1) {
            return link;
        }
        // if not able to parse the query params, then return only url
        var query_params = convert_queryparams_to_object(link[1]);
        if(!query_params) {
            return link;
        }
        // form query_params without alert_message
        var actual_url = link[0] + "?";
        $.each(query_params, function(k, v){
            if(k != "alert_message") {
                actual_url += k + "=" + v + "&";
            }
        });
        // remove alert_message key from url state, so that it is not showed up again and again
        history.pushState(null, "", actual_url);
    }

    // list all urls to be used, whether ajax or redirect url
    Common.login_url = "/login/";
    Common.register_url = "/create-user/";
    Common.forgot_password_url = "/forgot-password/";
    Common.check_useravailable = "/user-exists/";
    Common.event_listing = "/events/";
    Common.post_event = "/post-events/"


    // list of all messages
    Common.mandatory_params = "Error: Mandatory parameters missing";
    Common.mobile_mandatory = "Error: Mobile number should be 10 digit integer";
    Common.forgot_password_message = "Error: Please enter username";
    Common.event_apply_disabled = "Unauthorized Access: Please Login as a Candidate to Apply & Work for events"

    Common.init = init;
    Common.forceregister = forceregister;
    Common.bind_onkeyup = bind_onkeyup;
    Common.redirect = redirect;
    Common.ajaxcall = ajaxcall;
    Common.is_param_exist = is_param_exist;
    Common.form_unique_params = form_unique_params;
    Common.verify_mandatory = verify_mandatory;
    Common.show_alert = show_alert;
    Common.remove_alert_message = remove_alert_message;

})($,(window.Common = window.Common || {}));
