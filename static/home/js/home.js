;(function($, Common, Home) {
    function init(options) {
        var user_logged_in = options.user
        // first page farzi js for scroller
        $(window).load(function() {
            $("html,body").scrollTop(0);
            setTimeout(function() {
                $(".first_dark_screen").slideUp(1500);
                setTimeout(function(){
                    $(".actual_home").show();
                }, 700);
                $(".wse_name").css({
                    position:'absolute'
                    }).slideUp(1000);/*.animate({
                        top:'50'},
                        1500
                    );*/
            }, 3000);
        });

        Common.bind_force_registration(user_logged_in);
        // force register
        /*$(".force-register").on('click', function() {
            // get user type to decide next action url
            var user_type = $(this).data('user_type');
            $('#user_role option[value="' + user_type + '"]').attr("selected","selected");

            if(user_type=='client') {
                var action = Common.post_event;
            } else {
                var action = Common.event_listing;
            }
            Common.forceregister(user_logged_in, action, false);
        });*/
    }
    
    Home.init = init;
})($, Common, (window.Home = window.Home || {} ))
