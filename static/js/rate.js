(function(){
    var eventType;
    /************check the broswer*****************/
    function checkBroswer(){
        var sUserAgent = navigator.userAgent.toLowerCase();
        var bIsIpad = sUserAgent.match(/ipad/i) == "ipad";
        var bIsIphoneOs = sUserAgent.match(/iphone os/i) == "iphone os";
        var bIsMidp = sUserAgent.match(/midp/i) == "midp";
        var bIsUc7 = sUserAgent.match(/rv:1.2.3.4/i) == "rv:1.2.3.4";
        var bIsUc = sUserAgent.match(/ucweb/i) == "ucweb";
        var bIsAndroid = sUserAgent.match(/android/i) == "android";
        var bIsCE = sUserAgent.match(/windows phone/i) == "windows phone";
        var bIsWM = sUserAgent.match(/windows mobile/i) == "windows mobile";
        if (bIsIpad || bIsIphoneOs || bIsMidp || bIsUc7 || bIsUc || bIsAndroid || bIsCE || bIsWM) {
            return true;
        } else {
            return false;
        }
    }

    if(checkBroswer()){
        eventType = "tap";
    }else {
        eventType = "click";
    }

    /**
     * select unique rate
     */
    $(".rate .row a").on(eventType,function(e){
        e.stopPropagation();
        $a = $(this);

        if ($a.hasClass('select')) {
            //$a.removeClass('select');
        }
        else {
            var item;
            if ($a.hasClass('check-in')){
                item = $(".not-check-in");
                $("#check_in").val("1");
            }
            else if ($a.hasClass('not-check-in')){
                item = $(".check-in");
                $("#check_in").val("0");
            }
            else if($a.hasClass('point')){
                item = $(".point");
                $("#rate").val($a.html());
            }
            else {
                return;
            }
            item.removeClass('select');
            $a.addClass('select');
        }
    });

    /**
     * rate submit event
     */
    $(".rate .row .submit").on(eventType,function(e) {
        if ($("#rate").val() == "" ) {
            window.showTip('请给老师打个分');
            return;
        }
        else if ($("#check_in").val() == "") {
            window.showTip('请选择老师是否点名');
            return;
        }
        $("#rate-form").submit();
    });

    /**
     * comment submit event
     */
    $(".comment .submit").on(eventType,function(e) {
        content = $("#comment").val();
        //content.replace(' ','');
        if (content == "" || content.length <3 ) {
            window.showTip('至少要写3个字哦:(');
            return;
        }
        if (content.length >=800 ) {
            window.showTip('最多800个字哦:(');
            return;
        }
        var forbiddenWords = [
            '好老师',
            '好',
            '爽',
            '还行',
            '挺好的',
            '不错',
            '呵呵',
        ];
        for(i = 0;i < forbiddenWords.length; i++) {
            if (content == forbiddenWords[i]) {
                window.showTip('内容过于简单哦:(');
                return;
            }
        }
        $("#comment-form").submit();
    });

})();

function rateComment(a, pk, type) {
    var $a = $(a);
    var $count = $('.'+pk+'-count');
    var count = parseInt($count.text());
    var len = $count.text().length;
    var result;

    if ($a.hasClass('highlight')) return;
    if ($a.parent().children('.up.highlight').length) count--;
    if ($a.parent().children('.down.highlight').length) count++;

    $a.parent().children('a').removeClass('highlight');

    $a.addClass('highlight');

    if (type == 'like') {
        count++;
    }
    else {
        count--;
    }

    result = count.toString();
    for (var i = 0; i < len - count.toString().length; i+=2) {
        result = '&nbsp;'+result+'&nbsp;';
    }
    $count.html(result);

    $.get(
        '/comment/' + pk + '/rate',
        {'type':type}
    );
}

function reportComment(pk) {
    result = confirm("如果您觉得这条评论包含不当言论,\n您可以点击确认进行举报 🙉");
    if (result) {
        $.get(
          '/comment/' + pk + '/report',
            function(data,status){
                if (data == '1') {
                    alert("举报成功,我们会尽快核实 👀");
                }
            }
        );
    }
}

var commentPage = 0;
var commentsIsLoading = false;
function loadMoreComments(tid, order_by, callback) {
    if (commentsIsLoading) return;
    
    commentsIsLoading = true;
    
    $.get(
        '/teacher/' + tid + '/comment_list',
        {
            'page': commentPage++,
            'order_by':order_by
        },
        function (data, status) {
            if (!data.length) {
                if (typeof callback !== "undefined") {
                    callback(false);
                }
                return;
            }
            
            var container = $('#comment-container');
            container.html(container.html() + data);
            commentsIsLoading = false;
            
            if (typeof callback !== "undefined") {
                callback(true);
            }
        }
    )
}


function isScrolledIntoView(elem)
{
    if (!elem.length) return false;
    
    var docViewTop = $(window).scrollTop();
    var docViewBottom = docViewTop + $(window).height();

    var elemTop = $(elem).offset().top;
    var elemBottom = elemTop + $(elem).height();

    return ((elemBottom <= docViewBottom) && (elemTop >= docViewTop));
}