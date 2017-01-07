$(function(){

    //Horizontal Scrolling of Divs When Div is Clicked

    var index = 1, mar = 0;
    var childCount = $('.rightPanel').children().length;
    var parentWidth = parseInt($('.rightPanel').css("width"));

    $('.rightPanel').on('click', '.next', function(){

        var current = $(this);
        var present = $(".current");

        var width = parseInt($(present).css("width"));

        mar += Math.ceil((100*width)/parentWidth);

        $(present).removeClass("current");
        $(current).removeClass("next");
        $(current).addClass("current");

        $('.rightPanel').css("transform", "translateX(-" + mar + "%)");

        if(index != childCount){

            index++;
            var nextEl = $('.rightPanel .box:nth-child('+(index+1)+')');
            $(nextEl).addClass("next");
        }
        else{

            var presentEl = $('.rightPanel .box:nth-child(1)');
            $(presentEl).addClass("current");
            var nextEl = $('.rightPanel .box:nth-child(2)');
            $(nextEl).addClass("next");
            index = 1;
        }
    });

    // Changing the active menu item on click

    $('.jspPane a').click(function(e){

        e.preventDefault();
        $('.jspPane a span').removeClass("active");
        var child = $(this).children();
        $(child[0]).addClass("active");
    })
});

