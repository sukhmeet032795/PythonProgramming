$(function() {

    $(".like").click(function(e){

        var el = $(e.currentTarget);
        var blogParent = $(el).parents()[2];
        var blogId = $(blogParent).attr("id");
        var data = { "blogId" : blogId };

        likeAjax = $.ajax({
            type: 'POST',
            url: "/likeBlog",
            data: data,
            dataType: 'json',
            success: function(response){

                if(response.status == "success"){

                    $(el).parent().next(".post-likes").find("span").text("" + response.count)
                    var element = $(el).find("p");
                    if (response.msg == "liked"){

                        $(element).html("Liked");
                    }
                    else if (response.msg == "unliked"){

                        $(element).html("Like")
                    }
                }
                else if(response.status == "error"){

                    if(response.msg == "nouser"){

                        Materialize.toast("Please login to continue", 4000, 'rounded');
                        window.location.href = "/login";
                    }
                    else if(response.msg == "selflike"){

                        Materialize.toast("You can't like your own post", 4000, 'rounded');
                    }
                }
            },
            error: function(response){

                Materialize.toast("Something's Not Right", 4000, 'rounded');
            }
        });
    });

    $("input[name='comment']").keypress(function(e){

        if(e.keyCode == 13){
            $(this).focusout();
        }
    });

    $("input[name='comment']").on("focusout", function(e){

        var el = e.currentTarget
        var comment_val = $(el).val();
        var blogParent = $(el).parents()[4];
        var blogId = $(blogParent).attr("id");
        var data = { "blogId" : blogId, "comment" : comment_val, "status" : "createComment" };

        if (comment_val == "")
            return

        commentAjax = $.ajax({
            type: 'POST',
            url: "/commentBlog",
            data: data,
            dataType: 'json',
            success: function(response){

                $(el).val("");
                if(response.status == "success"){

                    if(response.msg == "commented"){

                        var html = "<div class='comment' id = '" + (response.comment.id) + "'><p class='commentBy'>"+ (response.comment.name) +"</p><p class='commentContent'>"+ (response.comment.content) +"</p><i class='fa fa-times deleteComment' aria-hidden='true'></i></div>"

                        var parent = $(el).parents()[2];
                        var showCommentsEl = $(parent).find(".show-comments");
                        $(showCommentsEl).prepend(html);
                    }
                }
                else if(response.status == "error"){

                    if(response.msg == "nouser"){

                        Materialize.toast("Please login to continue", 4000, 'rounded');
                        window.location.href = "/login";
                    }
                }
            },
            error: function(response){

                Materialize.toast("Something's Not Right", 4000, 'rounded');
            }
        });
    });

    $(".show-comments").on("click", ".deleteComment", function(e){

        var el = e.currentTarget;
        var commentId = $(el).parent().attr("id");
        var blogParent = $(el).parents()[4];
        var blogId = $(blogParent).attr("id");
        var data = { "commentId" : commentId, "status" : "deleteComment", "blogId" : blogId }
        console.log(data);

        delComment = $.ajax({
            type: 'POST',
            url: "/commentBlog",
            data: data,
            dataType: 'json',
            success: function(response){

                if(response.status == "success"){

                    if(response.msg == "uncommented"){

                        var parent = $(el).parent();
                        $(parent).remove();
                    }
                }
                else if(response.status == "error"){

                    if(response.msg == "nouser"){

                        Materialize.toast("Please login to continue", 4000, 'rounded');
                        window.location.href = "/login";
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
                    }
                }
                else if(response.status == "error"){

                    if(response.msg == "nouser"){

                        Materialize.toast("Please login to continue", 4000, 'rounded');
                        window.location.href = "/login";
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

    $(".editPost").click(function(e){

        var el = e.currentTarget;
        var blogId = $($(el).parents()[3]).attr("id");
        window.location.href = "/newPost/" + blogId;
    });
});