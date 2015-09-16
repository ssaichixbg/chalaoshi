(function(){
    /*****提示框的显隐*****/
    $content = $("#search-content");
    $content.on('input',function(e){
        input = $(this).val();
        $list = $('#result-list');
        if (input.length > 0) {
            $list.removeClass('hidden');
            $list.html('');
            $('#loading').removeClass('hidden');
            $.get(
                '/search',
                {'q':input},
                function(response){
                    $('#loading').addClass('hidden');
                    if (response.length>0) {
                        $list.html(response);
                    }
                    else {
                        $list.html('<a class="help" href="/feedback">没有要找的老师？</a>');
                    }
                }
            )
        }
        else {
            $list.addClass('hidden');
            $list.html('');
        }
    });
    $content.on('focus',function(e) {
        $('.main').addClass('fade');
        $('.copyright').addClass('fade');
        $('.footer').addClass('fade');
    });
    $content.on('blur',function(e) {
        $('.main').removeClass('fade');
        $('.copyright').removeClass('fade');
        $('.footer').removeClass('fade');

    });
})();