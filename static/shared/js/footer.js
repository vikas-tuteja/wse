;(function($,Common,Footer){
    function init(options) {
        $("#footer_submit").on('click', function(){
            var email = $("#footer_email").val();
            var mobile = $("#footer_mobile").val();
            if(!email) {
                alert("Please enter email id");
            }
            else if(!mobile) {
                alert("Please enter mobile");
            }
            else {
                var data = {
                    'email': email,
                    'mobile': mobile
                }
                var x = Common.ajaxcall('/create-user/', 'POST', data);
                x.success(function(resp){
                    // show alert
                    Common.show_alert(resp.message);
                    // TODO change sign in icon to my profile icon
                });
            }
        });

        // alert message from url GET
        if(options.alert_message) {
            Common.show_alert(options.alert_message)
        }

    }
    
    Footer.init = init;

})($,Common,(window.Footer = window.Footer || {}));
