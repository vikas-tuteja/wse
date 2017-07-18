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
        $(".requirement_apply").on('click', function() {
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

            var gender = $("#gender:checked").val();
            var duration = $("#duration:checked").val();
            $("#type:checked").each(function (){
                type += $(this).val() + ",";
            });

            if(gender && gender != undefined) {
                url = Common.form_unique_params('gender', gender, url, false);
            }
            if(type) {
                url = Common.form_unique_params('requirement', type, url, false);
            }
            if(duration) {
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
            window.location.href = document.URL.split('?')[0]
            
        });

        
    }
    

    function sort(elem, params) {
        $(elem).on('click', function() {
            var get_uniq_param = Common.form_unique_params('sort', elem);
            window.location.href = get_uniq_param;
        });
    }

    EventListing.init = init;

})($, Common, (window.EventListing= window.EventListing || {}))

