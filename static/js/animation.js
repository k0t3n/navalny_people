const scroller = new Scroller({
    el: document.querySelector('.person_scroller'),
    scrollbar: 'hidden',
    anchors: 'hidden',
    align: 'center',
    start: 'end'
});

function duckAnimation() {
    var $duck = $('.duck');
    if ($duck.css('top') === '62px') {
        $duck.animate({top: '30px'}, 700);
        $duck.animate({top: '62px'});
    }
}

$(document).ready(function () {
     $('.count').each(function () {
        $(this).prop('Counter',0).animate({
            Counter: $(this).text()
        }, {
            duration: 3000,
            easing: 'swing',
            step: function (now) {
                $(this).text(Math.ceil(now));
            }
        });
    });
    setTimeout(function() {
        scroller.scrollTo('start', 500);
    }, 500);
    $('.how_it_works-item a').on('click', function () {
        if ($(this).next().css('display') === 'none') {
            $(this).next().slideToggle('400');
            $(this).find('span').rotate(180);
        } else {
            $(this).next().slideToggle('400');
            $(this).find('span').rotate(0);
        }
    })
});