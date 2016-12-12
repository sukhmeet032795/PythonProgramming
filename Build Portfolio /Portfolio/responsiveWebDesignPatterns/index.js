$(function(){

    $('.fa-icon').click(function(e){

        e.preventDefault();
        var bool = $('.dark_blue').hasClass("showModal");
        console.log(bool);
        if(bool == true){

            $('.dark_blue').css("transform", "translate(0px, 0px)");
            $('.fa-icon').removeClass("slideRight");
        }

        else{

            $('.dark_blue').css("transform", "translate(-533px, 0px)");
            $('.fa-icon').addClass("slideRight");
        }
        e.stopPropagation();
    });

    $('.light_blue').click(function(e){

        e.preventDefault();
        $('.dark_blue').css("transform", "translate(-533px, 0px)");
        $('.fa-icon').removeClass("slideRight");
        e.stopPropagation();
    });
});