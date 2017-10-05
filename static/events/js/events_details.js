;(function($,Common,EventListing,EventDetail){

    function init(options) {
        $(".detail_tabs").on('click', function() {
        var elem = $(this).data('id');
        $('html,body').animate({
            scrollTop: $("#"+elem).offset().top},
            'slow');
        });
        EventListing.bind_apply_popup(options);
        EventListing.bind_requirement_popup(options);
        Common.empty_reqlist_hack();
        if(options.user) {
            Common.load_scripts_async(options.user, "/static/shared/js/guage.js", Common.guage_callback, Common.usermeter);
        }
        Common.load_iframe_async("fb");
    }

    EventDetail.init = init;

})($, Common, EventListing, (window.EventDetail = window.EventDetail || {}))
