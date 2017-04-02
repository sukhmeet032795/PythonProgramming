$(function(){

    var clicks = 0;

    $(".kittenClass").click(function(){

        clicks = clicks + 1;
        $("#clicks").html(clicks + " clicks");
    });
})