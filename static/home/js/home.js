;(function($, Common, Home) {
    function init() {
        $(window).load(function() {
        $("html,body").scrollTop(0);
        setTimeout(function() {
            $(".first_dark_screen").slideUp(1500);
            $(".wse_name").css({
                position:'absolute'
                }).slideUp(1000);/*.animate({
                    top:'50'},
                    1500
                );*/
        }, 3000);
        $(".wse_name");
});
    }
    
    Home.init = init;
})($, Common, (window.Home = window.Home || {} ))
