$(document).ready(function(){
    $("#id_regular_expression_1").on('change', function(){
        $.ajax({
            url:"/seo/get_named_url_list/",
            method:"GET",
            }).done(function(patterns){
                var options='';
                $.each(patterns.results, function(i, item){
                    options += '<option value="' + item[0] + '">' + item[1] + '</option>';
                });
                $("#id_path").replaceWith(
                    '<select name="path" id="path">' + options + '</select>'
                );
            });
    });
});
