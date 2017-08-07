;(function($,Common,EventDetail){

    function init(options) {
        $(".detail_tabs").on('click', function() {
        var elem = $(this).data('id');
        $('html,body').animate({
            scrollTop: $("#"+elem).offset().top},
            'slow');
        });
    }

    EventDetail.init = init;

})($, Common, (window.EventDetail = window.EventDetail || {}))
