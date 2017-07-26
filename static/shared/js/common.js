;(function($i, Common){
    
    function init(options) {
    }
    
    /*
    * input - search element id, result div id, ajax url, params
    * output - appends 10 results in the div
    */
    function bind_onkeyup(elem, resultelem, url, param) {
        $(elem).on('keyup', function(e) {
            var lis = '';
            $(resultelem).html(lis);

            if($.trim($(elem).val())) {
                var data = param + "=" + $.trim($(elem).val());
                var x = ajaxcall(url, 'GET', data);
            
                x.done(function(resp){
                    var response = resp.results;
                    $.each(response, function(i, e){
                        lis += '<a class="suggest_item" href="' + url + e.slug + '/">' + e.name + '</a>';
                    });
                    $(resultelem).html(lis);
                });
            }
        });
    }

    /*
    * make ajax call
    * input - url, method, param obj
    */
    function ajaxcall(url, method, param) {
        var response = $.ajax({
                        url:url,
                        method:method,
                        data:param,
                    });
        return response;
    }

    /*
    * onclick redirect to a url
    * input - elem, url, key, val_elem
    */
    function redirect(elem, url, key, val_elem) {
        $(elem).on('click', function(x) {
            var value = $.trim($(val_elem).val());
            if(value) {
                var href = url + "?" + key + "=" + value;
                window.location.href = href;
            }
        });
    }

    /*
    * returns true if get params exists in the current url
    */
    function is_param_exist() {
        if(document.URL.indexOf('?') != -1){
            return true;
        }
        return false;
    }

    /*
    * updates an existing queryparam or adds a new open
    * avoids same params to appear multiple times in the url 
    */
    function form_unique_params(key, data_elem, url=document.URL, sort=true) {
        var final_args = '';
        var args = url.split('?');
        if(sort) {
            var uniq = key + "=" + $(data_elem).data('order') + $(data_elem).data('key');
        } else {
            var uniq = key + "=" + data_elem;
        }
        if(args.length > 1) {
            $.each(args[1].split('&'), function(i, each) {
                if(each.indexOf(key) == -1) {
                    final_args += each + '&';
                }
            });
        }
        return args[0] + '?' + final_args + uniq
    }

    Common.init = init;
    Common.bind_onkeyup = bind_onkeyup;
    Common.redirect = redirect;
    Common.ajaxcall = ajaxcall;
    Common.is_param_exist = is_param_exist;
    Common.form_unique_params = form_unique_params;

})($,(window.Common = window.Common || {}));
