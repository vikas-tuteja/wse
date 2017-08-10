;(function($, Common, Home) {
    function init() {
        $(window).load(function() {
        setTimeout(function() {
            $(".first_dark_screen").slideUp(1500)
        }, 3000);
});
    }
    
    Home.init = init;
})($, Common, (window.Home = window.Home || {} ))
