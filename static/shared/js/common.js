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
                        lis += '<a class="suggest_item" href="' + url + e.slug + '/' + e.id + '/">' + e.name + '</a>';
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
            var uniq = key + "=" + encodeURIComponent(data_elem);
        }
        if(args.length > 1) {
            $.each(args[1].split('&'), function(i, each) {
                if(each.indexOf(key) == -1 && each != '') {
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
                if(elem) {
                    $(elem).html(error_message);
                    if($("#" + key).length) {
                        $("#" + key).css("border", "1px solid red");
                    }
                    $(".alert_message_error").show();
                } else {
                    Common.show_alert(error_message, false);
                }
            }

            // if mobile in key then, value should be integer and 10 digit long
            if(key.indexOf('mobile') != -1) {
                if(val.length != 10 || !$.isNumeric(val)) {
                    error += 1;
                    if(elem) {
                        $(elem).html(Common.mobile_mandatory);
                    } else {
                        Common.show_alert(error_message, false);
                    }
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
    * this fn is called, when a user clicks on requirement apply
    * 1. directly click on requirement apply
    * 2. clicks on requirement apply and then apply is called from login/register
    */
    function forceregister(user, action, isajax=true) {
        // if login -> ajax call to action & then reload
        if(user) {
            if(isajax==true || isajax=="true") {
                var x = Common.ajaxcall(action, 'GET', {});
                x.done(function(resp){
                    var url = Common.form_unique_params('alert_message', resp.message, document.URL.replace(/#.*$/, ""), false);
                    window.location.href = url;
                });
            } else {
                window.location.href = action;
            }
        }
        else {
            // show registration/login form if not logged in
            // if($("#close_req").length > 0) {
            //     $("#close_req")[0].click();
            // }
            window.location.href = "#closeModal"
            $(".sign-in").trigger('click');
            $("#action").val(action);
            $("#isajax").val(isajax);
            if(action) {
                $("#register-as").hide();
            }
        }
    }

    function bind_force_registration( is_logged_in ) {
        // force register
        $(".force-register").on('click', function() {
            // get user type to decide next action url
            var user_type = $(this).data('user_type');
            $('#user_role option[value="' + user_type + '"]').attr("selected","selected");

            if(user_type=='client') {
                var action = Common.post_event;
            } else {
                var action = Common.event_listing;
            }
            Common.forceregister(is_logged_in, action, false);
        });
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

    function show_alert(message, top=true) {
        // hide div if already open
        $("#alert_message").hide(); 
        if(top) {
            $('html,body').animate({
                scrollTop: (0)},
                'slow');
        }
        $("#alert_message").html(
            message + '<button class="btn-close" id="alert-close"><i class="fa fa-times" aria-hidden="true"></i></button>'
        //).fadeIn().fadeOut(20000, function() {});
        ).fadeIn();
        setTimeout(function() {     
           $("#alert_message").hide(); 
        },3000);
        
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

    /*
    * called after successful login
    * if action saved in login form, then complete the action using ajax
    * else just reload the same login
    */
    function after_login_process(resp) {
        var action = $("#action").val();
        $(".btn-close").trigger("click");
        var url = document.URL.replace(/#.*$/, "");
        /*/ if last character #, remove it
        if(url[url.length-1] == "#") {
            url = url.slice(0,-1)
        }*/
        url = Common.form_unique_params('alert_message', resp.message, url, false);
        if(action && action!='' && action!=null && action!=undefined) {
            var isajax=true;
            forceregister(true, action, $("#isajax").val())
        } else {
            window.location.href = url;
        }
    }

    function bind_key_escape() {
        $(document).keyup(function(e) {
            if (e.keyCode == 27) { // escape key maps to keycode `27`
                var close = $(".escape");
                if(close.length > 0 && close.css("display","block")) {
                    $.each(close, function(k, v) {
                        try { v.click(); }
                        catch(err) {}
                    });
                }
            }
        });

    }

    // list all urls to be used, whether ajax or redirect url
    Common.login_url = "/login/";
    Common.register_url = "/create-user/";
    Common.forgot_password_url = "/forgot-password/";
    Common.check_useravailable = "/user-exists/";
    Common.event_listing = "/events/";
    Common.post_event = "/post-events/";
    Common.update_profile = "/update-info/";
    Common.check_eventexists = "/event-exists/";


    // list of all messages
    Common.mandatory_params = "Error: Mandatory parameters missing";
    Common.mobile_mandatory = "Error: Mobile number should be 10 digit integer";
    Common.forgot_password_message = "Error: Please enter username";
    Common.event_apply_disabled = "Unauthorized Access: Only candidates can Apply &amp; Work for an event. Please Login as a Candidate"

    // post events page messages
    Common.max_schedule_limit_reached = "You can add a maximum of 4 different schedules for an event!!"
    Common.duplicate_schedule_alert = "Error: All schedules of an event must be unique."
    Common.add_existing_first = "Error: Please add existing schedule first."

    Common.add_existing_req_first = "Error: Please add existing requirement first."

    // requirement apply

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
    Common.after_login_process = after_login_process;
    Common.bind_key_escape = bind_key_escape;
    Common.bind_force_registration = bind_force_registration;

})($,(window.Common = window.Common || {}));
