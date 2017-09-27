;(function($,Common,PostEvent){


    function bind_datetime(num = "1") {
        /* datepicker */
        $.each(["#start_date_", "#end_date_"], function(i, elem) {
            $(elem + num).dateTimePicker();
        });
        
        /* timepicker */
        $('.timepicker').timepicker({
            timeFormat: 'HH:mm',                                           
            interval: 60,                                                  
            //minTime: '10',
            //maxTime: '23:59:59',                                         
            //defaultTime: '10',                                           
            startTime: '10:00:00',                                         
            //dynamic: false,
            dropdown: true,
            scrollbar: true
        });

    }

    function bind_event_exists() {
        $("#name").on("blur", function() {
            var event = $.trim($(this).val());
            if(event!="") {
                var x = Common.ajaxcall(Common.check_eventexists, 'GET', {'event':event})
                x.done(function(resp){
                    if(resp.status==true) {
                        $('#check_event_exists_result').html('<img class="square-img" src="/static/shared/images/cross.svg"> &nbsp; Event name already exists.')
                        $("#slug").val("");
                        $("#event_url").text('http://www.worksmartevents.com/events/{eventnamehere}/');
                        
                    } else {
                        $("#slug").val(resp.slug)
                        $("#event_url").text('http://www.worksmartevents.com/events/' + resp.slug + '/');
                        $('#check_event_exists_result').html('<img class="square-img"src="/static/shared/images/tick.png"> &nbsp; Event name Available.')
                    }
                });
            } else {
                $('#check_event_exists_result').html('<img class="square-img" src="/static/shared/images/cross.svg"> &nbsp; Event name cannot be blank.')
                $("#slug").val("");
                $("#event_url").text('http://www.worksmartevents.com/events/{eventnamehere}/');
                
            }
        });
    }

    function init(options){
        Common.bind_force_registration(options.user);
        bind_datetime();
        Common.remove_error_class("msform", "input");
        //bind_event_exists();
        //jQuery time
        var current_fs, next_fs, previous_fs; //fieldsets
        var left, opacity, scale; //fieldset properties which we will animate
        var animating; //flag to prevent quick multi-click glitches

        $(".next").click(function(){
            if(!validate($(this)[0].id)) return false;
            if(animating) return false;
            animating = true;
            
            current_fs = $(this).parent();
            next_fs = $(this).parent().next();
            
            //activate next step on progressbar using the index of next_fs
            $("#progressbar li").eq($("fieldset").index(next_fs)).addClass("active");
            
            //show the next fieldset
            next_fs.show(); 
            //hide the current fieldset with style
            current_fs.animate({opacity: 0}, {
                step: function(now, mx) {
                    //as the opacity of current_fs reduces to 0 - stored in "now"
                    //1. scale current_fs down to 80%
                    scale = 1 - (1 - now) * 0.2;
                    //2. bring next_fs from the right(50%)
                    left = (now * 50)+"%";
                    //3. increase opacity of next_fs to 1 as it moves in
                    opacity = 1 - now;
                    current_fs.css({'transform': 'scale('+scale+')'});
                    next_fs.css({'left': left, 'opacity': opacity});
                }, 
                duration: 800, 
                complete: function(){
                    current_fs.hide();
                    animating = false;
                }, 
                //this comes from the custom easing plugin
                easing: 'easeInOutBack'
            });
        });
        $(".previous").click(function(){
            if(animating) return false;
            animating = true;
            
            current_fs = $(this).parent();
            previous_fs = $(this).parent().prev();
            
            //de-activate current step on progressbar
            $("#progressbar li").eq($("fieldset").index(current_fs)).removeClass("active");
            
            //show the previous fieldset
            previous_fs.show(); 
            //hide the current fieldset with style
            current_fs.animate({opacity: 0}, {
                step: function(now, mx) {
                    //as the opacity of current_fs reduces to 0 - stored in "now"
                    //1. scale previous_fs from 80% to 100%
                    scale = 0.8 + (1 - now) * 0.2;
                    //2. take current_fs to the right(50%) - from 0%
                    left = ((1-now) * 50)+"%";
                    //3. increase opacity of previous_fs to 1 as it moves in
                    opacity = 1 - now;
                    current_fs.css({'left': left});
                    previous_fs.css({'transform': 'scale('+scale+')', 'opacity': opacity});
                }, 
                duration: 800, 
                complete: function(){
                    current_fs.hide();
                    animating = false;
                }, 
                //this comes from the custom easing plugin
                easing: 'easeInOutBack'
            });
        });
    }

    // add more schedule validations and logic
    var default_schedule_cnt = 1;
    var unique_start_dates = [];
    var unique_end_dates = [];
    $(document).on('click', '.add_more_schedule', function(x) {
        x.preventDefault();
 
        // check if one filled, only then show another
        var all_mandat = ['start_date_' + default_schedule_cnt,
                        'end_date_' + default_schedule_cnt,
                        'start_time_' + default_schedule_cnt,
                        'end_time_' + default_schedule_cnt];

        var mandat_check = true;
        $.each(all_mandat, function(k,v) {
            if($("#"+v).val() == '') {
                Common.show_alert(Common.add_existing_first, false);
                mandat_check = false;
                return false;
            }
        });

        if(!mandat_check) {
            return false;
        }

        // no duplicacy allowed
        var dates_check = true;
        if($.inArray( $("#start_date_" + default_schedule_cnt ).val(), unique_start_dates) != -1) {
            Common.show_alert(Common.duplicate_schedule_alert, false);
            dates_check = false;
            return false;
        } else {
            unique_start_dates.push($("#start_date_" + default_schedule_cnt).val())
        }

        if($.inArray( $("#end_date_" + default_schedule_cnt ).val(), unique_end_dates) != -1) {
            Common.show_alert(Common.duplicate_schedule_alert, false);
            dates_check = false;
            return false;
        } else {
            unique_end_dates.push($("#end_date_" + default_schedule_cnt).val())
        }

        if(!dates_check) {
            return false;
        }

        // max limit 4
        if(default_schedule_cnt == 4) {
            Common.show_alert(Common.max_schedule_limit_reached, false);
            return false;
        }

        // logic to append div
        var schedule_div = '<div class="demo-div mt20px">' +
                            '<label class="js-date"><span>Start Date <b>*</b></span><input type="text" name="start_date_xxx" id="start_date_xxx" class=" input "/><span><img src="/static/shared/images/calendar-icon.png" class="medium-img "><span></label>' + 
                            '<label class="js-date"><span>End Date <b>*</b></span><input type="text" name="end_date_xxx" id="end_date_xxx" class=" input "/><span><img src="/static/shared/images/calendar-icon.png" class="medium-img "><span></label>' +
                            '<label class="js-time"><span>Start Time <b>*</b></span><input type="text" name="start_time_xxx" id="start_time_xxx" class=" input timepicker "/><span><img src="/static/shared/images/clock1.jpg" class="square-img "><span></label>' +
                            '<label class="js-time"><span>End Time <b>*</b></span><input type="text" name="end_time_xxx" id="end_time_xxx" class=" input timepicker "/><span><img src="/static/shared/images/clock1.jpg" class="square-img "><span></label>' +
                            '</div>';
        
        default_schedule_cnt = append_html(default_schedule_cnt, schedule_div, '.schedules');
        bind_datetime(default_schedule_cnt);
    });

    // add more requirements validations and logic 
    var default_req_cnt = 1;
    $(document).on('click', '.add_more_requirements', function(x) {

        // check if all parameters are filled
        var params = {
            'candidate_type': $('#candidate_type_'+default_req_cnt).val(),
            'gender': $('#gender_'+default_req_cnt).val(),
            'count': $('#no_of_candidates_'+default_req_cnt).val(),
            //'no_of_days': $('#no_of_days_'+default_req_cnt).val(),
            'pay_per_day': $('#daily_wage_per_candidate_'+default_req_cnt).val(),
            //'education': $('#education_'+default_req_cnt).val(),
            //'language': $('#communication_criteria_'+default_req_cnt).val(),
            'dress_code': $('#dress_code_'+default_req_cnt).val(),
        }
        var verify = Common.verify_mandatory(params, false, Common.add_existing_req_first);
        if(!verify) {
            return false;
        }
        default_req_cnt++ ;
        // if all validations pass, then show div 2
        $("#req_div_" + default_req_cnt ).slideDown();
    });
    

    // briefin div show / hide
    $(".is_screening").on('click', function() {
        var val = $(this).val();
        if(val == "1") {
            $(".briefing_div").slideDown();
        }
        else {
            $(".briefing_div").slideUp();
        }
    });
    function append_html(counter, html, elem) {
        counter += 1;
        html = html.replace(/xxx/g, counter.toString());
        $(elem).append(html);
        return counter;
    }

    function validate(elem_id) {
       var id_param_map = {
            'post_events_1' : {
                'name': $('#name').val(),
                'venue': $('#venue').val(),
                'city': $('#city').val(),
                'area': $('#area').val(),
                'contact_person_number': $('#contact_person_number').val(),
                'start_date_1': $('#start_date_1').val(),
                'end_date_1': $('#end_date_1').val(),
                'start_time_1': $('#start_time_1').val(),
                'end_time_1': $('#end_time_1').val(),
            },
            'post_events_2' : {
                //'short_description': $('#short_description').val(),
                //'payments': $('#payments').val(),
            },
            'post_events_3' : {
                'candidate_type_1': $('#candidate_type_1').val(),
                'gender_1': $('#gender_1').val(),
                'no_of_candidates_1': $('#no_of_candidates_1').val(),
                //'no_of_days_1': $('#no_of_days_1').val(),
                'dress_code_1': $('#dress_code_1').val(),
                'daily_wage_per_candidate_1': $('#daily_wage_per_candidate_1').val()
            },
            'post_events' : {
                'short_description': $('#short_description').val(),
                'payments': $('#payments').val(),
            }
        }
        var verify = Common.verify_mandatory(id_param_map[elem_id], true, Common.mandatory_params);
        if(!verify) return false;
        else {
            if(elem_id!='post_events') return true;
            else {
                // do final post events page validation first
                var final_valid = true;
                $.each(["1", "2", "3"], function(k, n) {
                    if($("#tnc_" + n).is(":checked")==false && final_valid==true) {
                        Common.show_alert(Common.tnc, false);
                        final_valid = false;
                    }
                });
                if(!final_valid) return false;

                // form all input values dict and save it using ajax
                var values = {};
                $.each($('#msform').serializeArray(), function(i, field) {
                    values[field.name] = field.value;
                });

                var x = Common.ajaxcall(Common.post_event, 'POST', values)
                x.done(function(resp){
                    if(resp.status==true) {
                        window.location.href = '/events/' + resp.slug + '/' + resp.id +  '/?alert_message=' + resp.message
                    }
                });
            }
        }
    }

    PostEvent.init = init;

})($,Common, (window.PostEvent = window.PostEvent || {}));
