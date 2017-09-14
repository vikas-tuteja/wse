;(function($, Common, Home) {
    function init(options) {

        var user_logged_in = options.user

        // if this is NOT the first visit
        if (sessionStorage.getItem('firstVisit') === "1") {
            $(".wse_name").hide();
            $(".actual_home").show();

        } else {
            // first page  first visit farzi js for scroller
            $(window).load(function() {
                $("html,body").scrollTop(0);
                $(".wse_name").show();
                $(".first_dark_screen").show();
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
            sessionStorage.setItem('firstVisit', '1');
        }

        Common.bind_force_registration(user_logged_in);
    }
    
    Home.init = init;
})($, Common, (window.Home = window.Home || {} ))
