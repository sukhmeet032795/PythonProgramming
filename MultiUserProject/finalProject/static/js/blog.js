$(function() {

    $(".statusBar").css("display", "none");
    $(".post-likes").css("display", "none");
    $(".statusBar").css("display", "none");

    $(".deletePost").click(function(e){

        var el = e.currentTarget;
        var blogId = $($(el).parents()[3]).attr("id");
        var data = {"blogId" : blogId};

        delBlog = $.ajax({
            type: 'POST',
            url: "/deleteBlog",
            data: data,
            dataType: 'json',
            success: function(response){

                if(response.status == "success"){

                    if(response.msg == "blogDeleted"){

                        $($(el).parents()[3]).remove();
                        window.location.href = "/"
                    }
                }
                else if(response.status == "error"){

                    if(response.msg == "nouser"){

                        Materialize.toast("Please login to continue", 2000, 'rounded');
                        setTimeout(function() {
                            window.location.href = "/login";
                        }, 2000);
                    }
                    else if(response.msg == "otheruser"){

                        Materialize.toast("You can't delete other's reviews", 4000, 'rounded');
                    }
                }
            },
            error: function(response){

                Materialize.toast("Something's Not Right", 4000, 'rounded');
            }
        });
    });
});