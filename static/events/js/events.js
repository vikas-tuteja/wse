;(function($,Common,EventListing) { 
    function init(options){
        // search box functionality
        Common.bind_onkeyup(
            '#search', 
            '#search_results',
            '/events/',
            'name'
        )
        
        // go button redirect
        Common.redirect(
            '#go',
            '/events/',
            'name',
            '#search'
        )
        
        // bind popup
        $(".event_apply").on('click', function() {
            // if client, then on apply disabled
            if(options.accessibility == "False") {
                Common.show_alert(Common.event_apply_disabled)
            }
            else {
                var event_slug = $(this).attr('id').split('~~');
                var a = Common.ajaxcall("/events/requirements/" + event_slug[0] + "/", 'GET', {'format':'json'})
                a.done(function(resp){
                    var res= 'Requirement for ' + event_slug[1] ;
                    $.each(resp.results.results, function(idx, elem){
                        res += '<div class="req_list">' +
                            elem.id +
                            elem.event_slug +
                            elem.candidate_type +
                            elem.gender +
                            elem.no_of_candidates +
                            elem.daily_wage_per_candidate +
                            elem.dress_code +
                            elem.candidate_class + 
                            elem.communication_criteria +
                            elem.gender + '</div>';
                    });
                    $("#requirement_box").html(res);
                });
                window.location.href = "#openModal"
            }
        });

        // sorting functionality
        params = Common.is_param_exist();
        sort('#sort_name', params);
        sort('#sort_date', params);

        // apply filters
        $("#apply").on('click', function() {
            // TODO ask pawan about area filters
            var url = '';
            var type = '';
            var area_url = '';
            var area = [];

            var gender = $("#gender:checked").val();
            var duration = $("#duration:checked").val();
            $("#area:checked").each(function (idx, val){
                if(idx==0) {
                    area_url = $(this).val();
                }
                area.push($(this).val());
            });
            $("#type:checked").each(function (){
                type += $(this).val() + ",";
            });

            // area comes in url not queryparams + TODO check from PAWAN
            if(area_url) {
                url = '/events-in-' + area_url + '/';
                if(area.length > 0 ) {
                    url = Common.form_unique_params('area', area, url, false);
                }
            }
            if(gender && gender != undefined) {
                url = Common.form_unique_params('gender', gender, url, false);
            }
            if(type) {
                url = Common.form_unique_params('requirement', type, url, false);
            }
            if(duration && duration != undefined) {
                url = Common.form_unique_params('duration', duration, url, false);
            }

            // finally check if any filters applied
            if(url) {
                window.location.href = url
            }
            else {
                alert("Please select atleast one filter!!");
            }
        });

        // clear all filter
        $("#clear").on('click', function() {
            $.each(["gender","duration"], function(idx, elem){
                $("#"+elem).removeAttr("checked");
            });
            $.each(["type","area"], function(idx, elem){
                $("#"+elem+":checked").removeAttr("checked");
            });
            window.location.href = '/events/';
            
        });

        // bind requirement apply on click
        $("#requirement_apply").on('click', function() {
            var ajaxurl = "/events/apply/" + $(this).id;
            Common.forceregister(
                options.user,
                ajaxurl,
                true
             )
        });
        /*$("#requirement_apply").on('click', function() {
            var x = Common.ajaxcall(, 'POST', {})
            x.done(function(resp) {
                alert(resp.status + ' -- ' + resp.message);
            });
        });*/
    }
    

    function sort(elem, params) {
        $(elem).on('click', function() {
            var get_uniq_param = Common.form_unique_params('sort', elem);
            window.location.href = get_uniq_param;
        });
    }

    EventListing.init = init;

})($, Common, (window.EventListing= window.EventListing || {}))

