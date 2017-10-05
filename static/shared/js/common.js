;(function($, Common){
    
    function init(options) {
    }
    
    function guage_callback(meter_pointer) {
        var opts = {
            angle: -0.2, // The span of the gauge arc
            lineWidth: 0.2, // The line thickness
            radiusScale: 1, // Relative radius
            pointer: {
                length: 0.57, // // Relative to gauge radius
                strokeWidth: 0.033, // The thickness
                color: '#000000' // Fill color
          },
            limitMax: false,     // If false, max value increases automatically if value > maxValue
            limitMin: false,     // If true, the min value of the gauge will be fixed
            colorStart: '#6FADCF',   // Colors
            colorStop: '#8FC0DA',    // just experiment with them
            strokeColor: '#E0E0E0',  // to see which ones work best for you
            generateGradient: true,
            highDpiSupport: true,     // High resolution support
            staticLabels: {
            font: "10px sans-serif",  // Specifies font
            labels: [0, 20, 40, 60, 80, 100],  // Print labels at these values
            color: "#000000",  // Optional: Label text color
            fractionDigits: 0  // Optional: Numerical precision. 0=round off.
            },
            staticZones: [
                {strokeStyle: "#F03E3E", min: 0, max: 20}, // Red from 100 to 130
                {strokeStyle: "#FFDD00", min: 20, max: 40}, // yellow
                {strokeStyle: "#6fadcf", min: 40, max: 100}, // blue
                ],
        };
        var percentColors = [[0.0, "red" ], [0.20, "#f9c802"], [1.0, "#ff0000"]];
        
        var target = document.getElementById('usermeter'); // your canvas element
        var gauge = new Gauge(target).setOptions(opts); // create sexy gauge!
        gauge.maxValue = 100; // set max gauge value
        gauge.setMinValue(0);  // Prefer setter over gauge.minValue = 0
        gauge.animationSpeed = 22; // set animation speed (32 is default value)
        gauge.set(meter_pointer); // set actual value
    }

    function load_scripts_async(user_id, script_path, callback, ajax) {

        $.getScript( script_path )
          .done(function( script, textStatus ) {
                var data = {
                    'userid':user_id,
                    'format': 'json',
                }
                var x = ajaxcall(ajax, 'GET', data);
            
                x.done(function(resp){
                    guage_callback(resp.profile_completed);
                });           
          })
          .fail(function( jqxhr, settings, exception ) {
            console.log( 'Failed' );
        });
    }

    function load_iframe_async(which) {
        if(which=='fb') {
            $(window).load(function() {
                $('#fb_load').hide();
                $('#fb').attr('src', Common.fb);
            });
        }
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
        $.each(obj, function(key, val) {
            if(true) {
                // if any value blank, return false
                if($.trim(val) == '' ) {
                    error += 1;
                    if(elem===true) {
                        $('#' + key).css('border', '1px solid red');
                        Common.show_alert(error_message);
                    } else if(elem) { 
                        $(elem).html(error_message);
                        if($("#" + key).length) {
                            $('#' + key).css('border', '1px solid red');
                        }
                        $(".alert_message_error").show();
                    } else {
                        Common.show_alert(error_message, false);
                    }
                }

                // if mobile in key then, value should be integer and 10 digit long
                if(error==0) {
                    var integers = ['mobile', 'no_of_candidates', 'no_of_days', 'daily_wage_per_candidate', 'contact_person_number'];
                    $.each(integers, function(idx, each) {
                        if(key.indexOf(each) != -1) {
                            if(!$.isNumeric(val) || (key.indexOf('mobile')!=-1 && val.length != 10)) {
                                error += 1;
                                if(elem===true) {
                                    $('#' + key).css('border', '1px solid red');
                                    if(each=='contact_person_number') {
                                        Common.show_alert(Common.post_number);
                                    } else {
                                        Common.show_alert(Common.count_no_pay);
                                    }
                                } else if(elem){
                                    $(elem).html(Common.mobile_mandatory);
                                } else {
                                    Common.show_alert(error_message, false);
                                }
                            }
                        }
                    });
                }
            }
        });
        if(error==0) {
            return true;
        } else {
            return false;
        }
    }

    function bind_city_area_filter(pr, ch) {
        $("."+pr).on('change', function () {
            var x = Common.ajaxcall('/master/arealisting/', 'GET', {'city': $("."+pr+" option:selected").val() });
            x.done(function(resp){
                $("."+ch).find('option').remove()
                $.each(resp['results'], function (i, item) {
                    $('.'+ch).append($('<option>', { 
                        value: item.slug,
                        text : item.name
                    }));
                });
            });
        });    
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

    function empty_reqlist_hack() {
        if(document.URL.indexOf('#openModal') != -1 && $('#requirement_box').length >=1 && $('#requirement_box').val() == '') {
            window.location.href = '#closeModal';
        }
    }
    
    function remove_error_class(parentdiv, elem) {
        $('#'+ parentdiv + ' :' + elem).on('focus', function() {
            $(this).css('border', '0');
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
    Common.change_password = "/change-password/";
    Common.fb = "//www.facebook.com/plugins/like.php?href=https%3A%2F%2Fwww.facebook.com%2Fworksmartofficial&width=140&layout=button_count&action=like&size=small&show_faces=true&share=true&height=46&appId=1667073276882154";
    Common.usermeter = "/user-meter/";


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
    Common.count_no_pay = "Error: Count and pay per day should be numeric."
    Common.post_number = "Error: Contact number should be numberic."

    Common.password_length = "Error: New Password must be atleast 8 characters long."
    Common.passwords_mismatch = "Error: Password and confirm password must be same"
    Common.password = "Validation Error: Password & Confirm Passord must be same & must be 8 caharacters"
    Common.tnc = "Error: Please accept all Terms & Conditions."

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
    Common.empty_reqlist_hack = empty_reqlist_hack;
    Common.remove_error_class = remove_error_class;
    Common.bind_city_area_filter = bind_city_area_filter;
    Common.load_scripts_async = load_scripts_async;
    Common.load_iframe_async = load_iframe_async;
    Common.guage_callback = guage_callback;

})($,(window.Common = window.Common || {}));
