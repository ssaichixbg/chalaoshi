(function(){
    window.searchTeacher = function(keyword) {
        $('#loading').removeClass('hidden');
        $list = $('#result-list');
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
    };
    function hideList() {
        $list = $('#result-list');
        $list.addClass('hidden').html('');
    }
    function displayList() {
        $list = $('#result-list');
        $list.removeClass('hidden').html('');
    }
    /*****提示框的显隐*****/
    $content = $("#search-content");
    $content.on('input',function(e){
        input = $(this).val();
        if (input.length > 0) {
            displayList();
            window.searchTeacher(input);
        }
        else {
            hideList();
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

    // get pre-search
    if (search_url != "") {
        $list = $('#result-list');
        displayList();
        $('#loading').removeClass('hidden');
        $.get(
            '/search?'+search_url,
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
})();