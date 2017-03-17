$(function() {

    $('.modal').modal();

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

                    $(el).parent().next(".post-likes").find("span").text("" + response.count + " Likes")
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

                        Materialize.toast("Please login to continue", 2000, 'rounded');
                        setTimeout(function() {
                            window.location.href = "/login";
                        }, 2000);
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
        var data = { "blogId" : blogId, "comment" : comment_val, "status" : "createComment"};

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

                        var html = "<div class='comment' id = '" + (response.comment.id) + "'><div class='comment-content'><div class='commentBy'>"+ (response.comment.name) +"</div><div class='commentContent'>"+ (response.comment.content) +"</div></div><i class='material-icons dropdown-button' data-activates='drop_" + (response.comment.id) + "'>mode_edit</i><ul id='drop_" + (response.comment.id) + "' class='dropdown-content'><li><span class='modal-trigger editComment'>Edit Comment</span></li><li class='divider'></li><li><span class='deleteCommentDropdown'>Delete Comment</span></li></ul></div>"
                        var parent = $(el).parents()[2];
                        var showCommentsEl = $(parent).find(".show-comments");
                        $(showCommentsEl).prepend(html);
                        $(".dropdown-button").dropdown();
                    }
                }
                else if(response.status == "error"){

                    if(response.msg == "nouser"){

                        Materialize.toast("Please login to continue", 2000, 'rounded');
                        setTimeout(function() {
                            window.location.href = "/login";
                        }, 2000);
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
        console.log($(el).parents())
        var commentParent = $(el).parents()[0];
        var commentId = $(commentParent).attr("id");
        var blogParent = $(el).parents()[4];
        var blogId = $(blogParent).attr("id");
        var data = { "commentId" : commentId, "status" : "deleteComment", "blogId" : blogId }

        delComment = $.ajax({
            type: 'POST',
            url: "/commentBlog",
            data: data,
            dataType: 'json',
            success: function(response){

                if(response.status == "success"){

                    if(response.msg == "uncommented"){

                        $(commentParent).remove();
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

    $(".show-comments").on("click", ".deleteCommentDropdown", function(e){

        var el = e.currentTarget;
        console.log($(el).parents())
        var commentParent = $(el).parents()[2];
        var commentId = $(commentParent).attr("id");
        var blogParent = $(el).parents()[6];
        var blogId = $(blogParent).attr("id");
        var data = { "commentId" : commentId, "status" : "deleteComment", "blogId" : blogId }
        console.log(data)
        delComment = $.ajax({
            type: 'POST',
            url: "/commentBlog",
            data: data,
            dataType: 'json',
            success: function(response){

                if(response.status == "success"){

                    if(response.msg == "uncommented"){

                        $(commentParent).remove();
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

    $(".editPost").click(function(e){

        var el = e.currentTarget;
        var blogId = $($(el).parents()[3]).attr("id");
        window.location.href = "/editBlog/" + blogId;
    });

    $(".show-comments").on("click", ".editComment", function(e){

        var el = e.currentTarget;
        var element = $(el).parents()[2];
        var commentId = $(element).attr("id");
        var commentBody = $($(element).find(".commentContent")).html();

        $('#editCommentModal').modal('open');

        var modalEl = $(".write-comment-modal");
        $(modalEl).attr("id", commentId);

        var inputField = $(modalEl).find("#icon_comment");
        $(inputField).val(commentBody);
        $(inputField).trigger('autoresize');
    });

    $("input[name='comment-modal']").keypress(function(e){

        if(e.keyCode == 13){
            $(this).focusout();
        }
    });

    $("input[name='comment-modal']").on("focusout",function(e){

        var el = e.currentTarget;

        var commentId = $(".write-comment-modal").attr("id");
        var commentContent = $(el).val();
        var commentObj = {"id" : commentId, "content" : commentContent, "status" : "updateComment"};
        console.log(commentObj)

        updateCommentAjax = $.ajax({
            type: 'POST',
            url: "/commentBlog",
            data: commentObj,
            dataType: 'json',
            success: function(response){

                if(response.status == "success"){

                    if(response.msg == "updated"){

                        $('#editCommentModal').modal('close');
                        var commentEl = $(".show-comments #" + commentId)[0];
                        var container = $(commentEl).find(".commentContent")[0];
                        $(container).html(commentContent);
                    }
                }
                else if(response.status == "error"){

                }
            },
            error: function(response){

                Materialize.toast("Something's Not Right", 4000, 'rounded');
            }
        });
    });
});