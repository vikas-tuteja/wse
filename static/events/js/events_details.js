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
    }

    EventDetail.init = init;

})($, Common, EventListing, (window.EventDetail = window.EventDetail || {}))
