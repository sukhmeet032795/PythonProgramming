$(function(){

    var model = {

        currentCat = null,
        cats = []
    };

    var octopus = {

        setCurrent : function(cat){
            model.currentCat = cat;
        },
        getCurrent : function(){
            return model.currentCat;
        },
        getCats : function(){
            return model.cats;
        },
        getCat : function(index){
            cat = cats[index];
            view.render(cat);
        },
        incrementClicks :  function(index){
            cat = cats[index];
            cat.clicks += 1
            view.render(cat);
        },
        init : function(){

        }
    };

    var catListView = {

        init: function(){

            var catList = [];
            catList = $("#cat-labels-list");

            this.render():
        },
        render: function(){

            $(catList).html("");

            var objs = model.cats;

            for(var i = 0; i < objs.length; i++){

                var el = '<li id='+ objs[i].id +'>'+ objs[i].name +'</li>';

                $(el).on("click", function(){

                    octopus.setCurrent($(el).attr("id"));
                    catView.render();
                });

                catList.append(el);
            }
        }
    };

    var catView = {

        init: function(){

            var catDisplay = $(".catDisplay");
            var catName = $("#catName");
            var catImage = $("#catImage");
            var displayClicks = $("#displayClicks");

            $(catImage).on("click", function(){
                octopus.incrementClicks();
            });

            this.render();
        },

        render: function(){

            var currCat = octopus.getCurrent();
            $(catName).html(currCat.name);
            $(catImage).attr(src, currCat.url);
            $(displayClicks).html("The Number of Clicks are: " + currCat.clicks);
        }
    };
});