;(function($,MyProfile){

    function init(options){
        // default show only first div content and thus bg -select only first label
        $('div[id^="content-"]').css("display","none");

        $("#content-1").css("display","block");
        $("#label-1").addClass("bg-selected");


        // onclick label, show its respective content
        $('div[id^="label-"]').on('click', function() {
            $('div[id^="label-"]').removeClass("bg-selected");
            $(this).addClass("bg-selected");

            $('div[id^="content-"]').css("display","none");
            $('#content-'+$(this).data('num')).css("display","block");
        });
    }
    
    MyProfile.init = init;
})($, window.MyProfile= window.MyProfile || {})
