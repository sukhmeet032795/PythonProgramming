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

    //Redirect to my wall handler

    $(".myWall").click(function(e){

        window.location.href = "/wall";
    });

    $(".home").click(function(e){

        window.location.href = "/";
    });

    $("#homeLabel").click(function(e){

        window.location.href = "/";
    });

    //Adding a new blog

    $("#addBlog").click(function(e){

        checkUserAjax = $.ajax({
            type: 'GET',
            url: "/checkUser",
            dataType: 'json',
            success: function(response){

                if(response.status == "success"){

                    if(response.msg == "user"){

                        window.location.href = "/newPost";
                    }
                }
                else if(response.status == "error"){

                    if(response.msg == "nouser"){

                        Materialize.toast("Please login to continue", 1000, 'rounded');
                        setTimeout(function() {
                            window.location.href = "/login";
                        }, 1000);

                    }
                }
            },
            error: function(response){

                Materialize.toast("Something's Not Right", 4000, 'rounded');
            }
        });
    });
});