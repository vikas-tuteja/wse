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
                    // Common.show_alert(resp.message);
                    var url = document.URL
                    // if last character #, remove it
                    if(url[url.length-1] == "#") {
                        url = url.slice(0,-1)
                    }
                    url = Common.form_unique_params('alert_message', resp.message, url, false);
                    window.location.href = url;
                });
            }
        });

        // alert message from url GET is displayed here on every page
        if(options.alert_message) {
            Common.show_alert(options.alert_message)
            // remove alert message from get
            Common.remove_alert_message(document.URL);
        }
        
        // get and set city name in menubar
        $.get("https://ipinfo.io", function(response) {
            $(".current_city").html(response.city || 'Mumbai');
        }, "jsonp");

    }
    
    Footer.init = init;

})($,Common,(window.Footer = window.Footer || {}));
