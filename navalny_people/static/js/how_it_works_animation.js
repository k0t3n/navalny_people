$(document).ready(function () {
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