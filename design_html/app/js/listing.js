$(function(){

    $('.mobile-menu').on('click', function() {
        $('.main-nav').css('display', 'block');
        $('.right-menu').css('display', 'block');
        $('body').addClass('overhide');
    });

    $('.close-nav').on('click', function() {
        $('body').removeClass('overhide');
        $('.main-nav').css('display', '');
        $('.right-menu').css('display', '');
    });
});