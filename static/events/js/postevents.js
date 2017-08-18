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
    function init(options){
        bind_datetime();
        //jQuery time
        var current_fs, next_fs, previous_fs; //fieldsets
        var left, opacity, scale; //fieldset properties which we will animate
        var animating; //flag to prevent quick multi-click glitches

        $(".next").click(function(){
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
                            '<label class="event-label clearfix">' +
                            '<span>Start Date <b>*</b></span><input type="text" name="start_date_xxx" id="start_date_xxx" class="mt10px input small-input"/><img src="/static/shared/images/calendar-icon.png" class="medium-img mt10px">' + 
                            '<span>End Date <b>*</b></span><input type="text" name="end_date_xxx" id="end_date_xxx" class="mt10px input small-input"/><img src="/static/shared/images/calendar-icon.png" class="medium-img mt10px">' +
                            '<span>Start Time <b>*</b></span><input type="text" name="start_time_xxx" id="start_time_xxx" class="mt10px input timepicker small-input"/><img src="/static/shared/images/clock1.jpg" class="square-img mt10px">' +
                            '<span>End Time <b>*</b></span><input type="text" name="end_time_xxx" id="end_time_xxx" class="mt10px input timepicker small-input"/><img src="/static/shared/images/clock1.jpg" class="square-img mt10px">' +
                            '</label></div>';
        
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
            'count': $('#count_'+default_req_cnt).val(),
            'no_of_days': $('#no_of_days_'+default_req_cnt).val(),
            'pay_per_day': $('#pay_per_day_'+default_req_cnt).val(),
            'education': $('#education_'+default_req_cnt).val(),
            'language': $('#language_'+default_req_cnt).val(),
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
            $("#briefing_div").slideDown();
        }
        else {
            $("#briefing_div").slideUp();
        }
    });
    function append_html(counter, html, elem) {
        counter += 1;
        html = html.replace(/xxx/g, counter.toString());
        $(elem).append(html);
        return counter;
    }
    PostEvent.init = init;

})($,Common, (window.PostEvent = window.PostEvent || {}));