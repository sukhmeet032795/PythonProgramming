$(function(){

    //Handling redirection to signup and login page

    $("#loginLabel").click(function(e){

        window.location.href = "/login";
    });

    $("#signupLabel").click(function(e){

        window.location.href = "/signup";
    });

    //Handling redirection to main page on clicking header icon

    $(".headerImage img").click(function(e){

        window.location.href = "/";
    });

    //Handling Dropdowns(MaterialCss) on various pages

    $('.dropdown-button').dropdown();

    //Logout handler

    $(".logout").click(function(e){

        window.location.href = "/logout";
    });
});