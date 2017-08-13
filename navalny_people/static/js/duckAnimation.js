function duckAnimation() {
    var $duck = $('.duck');
    if ($duck.css('top') === '62px') {
        $duck.animate({top: '30px'}, 700);
        $duck.animate({top: '62px'});
    }
}