(function(){

})();
function changeCollege(value) {
    var $college_id = $('#college_id');
    if (value != $college_id.val) {
        $college_id.val(value);
        $('#college-form').submit();
    }

}