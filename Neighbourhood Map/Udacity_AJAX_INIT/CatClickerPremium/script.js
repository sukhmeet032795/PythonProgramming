$(function(){

    var model = {

        currentCat : null,
        showAdmin : false,
        cats : [
            {
                clicks : 0,
                name : 'Harold',
                url : 'https://s-media-cache-ak0.pinimg.com/736x/b6/e8/5f/b6e85f2631fd74df894418a7ac51abc3.jpg'
            },
            {
                clicks : 0,
                name : 'Maple',
                url : 'https://s-media-cache-ak0.pinimg.com/736x/65/09/0b/65090ba68e4d61f8f203a76a91e6cd29.jpg'
            },
            {
                clicks : 0,
                name : 'Grumpy Cat',
                url : 'http://i42.tinypic.com/9qv13l.jpg'
            },
            {
                clicks : 0,
                name : 'Marie',
                url : 'https://s-media-cache-ak0.pinimg.com/736x/d8/1f/53/d81f53608e1c359cfd14c770fa502a66.jpg'
            },
            {
                clicks : 0,
                name : 'Crookshanks',
                url : 'http://farm3.staticflickr.com/2831/12660151764_c25940554d.jpg'
            }
        ]
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
        incrementClicks :  function(){
            cat = model.currentCat;
            cat.clicks += 1
            catView.render();
        },
        init : function(){

            model.currentCat = model.cats[0];

            catListView.init();
            catView.init();
            adminView.init();
            adminView.hide();
        },
        checkAdminStatus: function(){
            return model.showAdmin;
        },
        adminSave: function(){

            model.getCurrent.name = adminView.name;
            model.getCurrent.url = adminView.url;
            model.getCurrent.clicks = parseInt($(adminView.clicks).val());
            catView.render();
            catListView.render();
            adminView.hide();
        },
        adminCancel: function(){

            adminView.hide();
        },
        adminShow: function(){

            if(model.showAdmin == false){

                model.showAdmin = true;
                adminView.show();
            }
            else if (model.adminShow === true) {
                model.adminShow = false;
                adminView.hide();
            }
        }
    };

    var catListView = {

        init: function(){

            this.catList = [];
            this.catList = $("#cat-labels-list");

            this.render();
        },
        render: function(){

            $(this.catList).html("");

            var cats = octopus.getCats();

            for(var i = 0; i < cats.length; i++){

                var cat = cats[i];

                el = document.createElement('li'); //create li element
                el.textContent = cat.name;

                $(el).click((function(cat){

                    return function(){

                        octopus.setCurrent(cat);
                        catView.render();
                    }
                })(cat));

                this.catList.append(el);
            }
        }
    };

    var catView = {

        init: function(){

            this.catDisplay = $(".catDisplay");
            this.catName = $("#catName");
            this.catImage = $("#catImage");
            this.displayClicks = $("#displayClicks");

            $(this.catImage).on("click", function(){
                octopus.incrementClicks();
            });

            this.render();
        },

        render: function(){

            var currCat = octopus.getCurrent();
            $(this.catName).html(currCat.name);
            $(this.catImage).attr("src", currCat.url);
            $(this.displayClicks).html("The Number of Clicks are: " + currCat.clicks);
        }
    };

    var adminView = {

        init: function(){

            this.name = $("#cat-name");
            this.url = $("#cat-url");
            this.clicks = $("#cat-clicks");
            this.submit = $("#submit");
            this.cancel = $("#cancel");
            this.admin = $("#admin");
            this.panel = $("#admin-panel");

            $(this.submit).click(function(){
                octopus.adminSave();
            });

            $(this.cancel).click(function(){
                octopus.adminCancel();
            });

            $(this.admin).click(function(){
                octopus.adminShow();
            });

            this.render();
        },

        render: function(){

            var currentCat = octopus.getCurrent();

            $(this.name).val(currentCat.name);
            $(this.url).val(currentCat.url);
            $(this.clicks).val(currentCat.clicks);
        },

        show: function(){

            $(this.panel).css("display", "block");
        },

        hide: function(){

            $(this.panel).css("display", "none");
        }
    }

    octopus.init();
});