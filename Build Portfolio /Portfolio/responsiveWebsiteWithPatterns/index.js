$(function(){

    $('.fa-icon').click(function(e){

        e.preventDefault();
        $('.nav__mobile').toggleClass("open");
        e.stopPropagaton();
    });

    $('main').click(function(e){

        $('.nav__mobile').removeClass("open");
        e.stopPropagaton();
    });
});