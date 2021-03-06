/* global $, Common */
;(function($,Common,EventListing) { 
    function bind_apply_popup(options) {
        // bind popup
        $(".event_apply").on('click', function() {
            // if client, then on apply disabled
            if(options.accessibility == "False") {
                Common.show_alert(Common.event_apply_disabled)
            }
            else {
                var event_slug = $(this).attr('id').split('~~');
                var a = Common.ajaxcall("/events/requirements/" + event_slug[2] + "/", 'GET', {'format':'json'})
                a.done(function(resp){
                    var res = '<p class="blue mt10px" style="font-weight:200 !important;padding-top:20px;"><b>Requirement for ' + event_slug[1] + '</b></p>';
                    var gender_meta = {'f':'Lady', 'm':'Gentleman', 'fplural': 'Ladies', 'mplural': 'Gents', 'a': 'Person', 'aplural': 'People'}
                    $.each(resp.results.results, function (idx, elem) {
                        if(elem.no_of_candidates>1){
                            elem.gender = elem.gender + 'plural';
                        }
                        var dress_code_img = '<img class="square-img" src = "/static/shared/images/cross.svg">';
                        if(elem.dress_code && elem.dress_code != null) {
                            dress_code_img = '<img class="square-img" src = "/static/shared/images/tick.png">';
                        }
                        res += '<div class="req_list">' +
                            '<div class="strip-head"><span>' + 
                            elem.candidate_type + '</span></div>' + 
                            '<div><table class="table">' + 
                            '<tr><td><b>' + elem.no_of_candidates + ' ' + gender_meta[elem.gender] + '</b> Required </td></tr>' +
                            '<tr><td><b>INR ' + elem.daily_wage_per_candidate + '</b> per day </td></tr>' +
                            '<tr><td>Dress Code ' + dress_code_img + '</td></tr>' +
                            '<tr><td>';

                        if(elem.communication_criteria && elem.communication_criteria != null ) {
                            res += elem.communication_criteria;
                        } else {
                            res += '&nbsp;';
                        }
                        res += '</td></tr><tr><td colspan=2><button data-id="' + elem.id + '" class="requirement_apply btn btn-blue mt-15">Apply</button></td></tr></table></div></div>';
                    });
                    $("#requirement_box").html(res);
                });
                window.location.href = "#openModal"
            }
        });

    }

    function show_filters_for_mobile() {
        $(".filters").on('click', function() {
            $("html,body").scrollTop(0);
            $('.left-fixed').css('left', '0');
            $('.left-fixed').css('position', 'relative');
            $('.left-fixed').css('width', '100%');
        });
    }

    function bind_requirement_popup(options) {
        // bind requirement apply on click
        $(document).on('click', '.requirement_apply', function(e) {
            var ajaxurl = '/events/apply/' + $(this).data('id') + '/';
            Common.forceregister(
                options.user,
                ajaxurl,
                true
             )
        });
    }

    function init(options){
        //escape key close event
        Common.empty_reqlist_hack();
        Common.bind_key_escape();
        show_filters_for_mobile();

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
        bind_apply_popup(options);

        // sorting functionality
        params = Common.is_param_exist();
        sort('#sort_name', params);
        sort('#sort_date', params);

        // apply filters
        $(".apply").on('click', function() {
            // TODO ask pawan about area filters
            var url = '';
            var type = '';
            var area_url = '';
            var area = [];
            var city_url = '';
            var city = [];

            var gender = $("#gender:checked").val();
            var duration = $("#duration:checked").val();
            $("#city:checked").each(function (idx, val){
                if(idx==0) {
                    city_url = $(this).val();
                }
                city.push($(this).val());
            });

            $("#area:checked").each(function (idx, val){
                if(idx==0) {
                    area_url = $(this).val();
                }
                area.push($(this).val());
            });
            $("#type:checked").each(function (){
                type += $(this).val() + ",";
            });

            if(city_url) {
                url = '/events-in-' + city_url + '-city/';
                if(city.length > 0 ) {
                    url = Common.form_unique_params('city', city, url, false);
                }
            }

            // area comes in url not queryparams
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

        $(window).resize(function(){
            if($('#search_results').is(':visible')){
                $('#search_results').css('max-width', $('#search').parent('div').width())
            }
        });

        $('#search').focus(function(){
            $('#search_results').css('max-width', $(this).parent('div').width());
        });

        bind_requirement_popup(options);
        if(options.user) {
            Common.load_scripts_async(options.user, "/static/shared/js/guage.js", Common.guage_callback, Common.usermeter);
        }
        Common.load_iframe_async("fb");
        Common.load_iframe_async("youtube");
    }
    

    function sort(elem, params) {
        $(elem).on('click', function() {
            var get_uniq_param = Common.form_unique_params('sort', elem);
            window.location.href = get_uniq_param;
        });
    }


    EventListing.init = init;
    EventListing.bind_apply_popup = bind_apply_popup;
    EventListing.bind_requirement_popup = bind_requirement_popup;
    

})($, Common, (window.EventListing= window.EventListing || {}))
