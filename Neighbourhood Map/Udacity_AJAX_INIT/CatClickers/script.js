$(function(){


    // Visuals
    //     The application should display a picture of a cat and a number of clicks.
    //     The specifics of the layout do not matter, so style it however you'd like.
    // Interaction
    //     The number of clicks should increment when the cat picture is clicked.

    var clicks = 0;

    $(".kittenClass").click(function(){

        clicks = clicks + 1;
        $("#clicks").html(clicks + " clicks");
    });

    // The application should display two cats. Each cat includes
    //     the cat's name
    //     a picture of the cat
    //     text showing the number of clicks
    // The specifics of the layout do not matter, so style it however you'd like.

    var cat = function(name, url){

        this.name = name;
        this.url = url;
        this.clicks = 0;
    };

    var cats = []

    var tommy = new cat("Tommy", "http://placekitten.com/g/500/500");
    var hilfiger = new cat("Hilfiger", "http://placekitten.com/g/500/500");

    cats.push(tommy, hilfiger);

    var container = $(".cat-container2");

    for(var i = 0; i < cats.length; i++){

        var currentEl = cats[i];
        $(container).append("<div class='cat' id = '"+ currentEl.name +"'><img src='"+ currentEl.url +"' class='kittenClass' id= '"+i+"'><p id='clicks'>"+ currentEl.clicks +" clicks</p></div>");
    }

    $(".cat").click(function(e){

        var el = e.target.parentElement;
        var id = el.childNodes[0].id;
        cats[id].clicks += 1;
        $(el.childNodes[1]).html(cats[id].clicks + " Clicks");
    });

    // The application should display
    //     a list of at least 5 cats, listed by name
    //     an area to display the selected cat

    // In the cat display area, the following should be displayed
    //     the cat's name
    //     a picture of the cat
    //     text showing the number of clicks

    var catPremium = function(name, url){

        var name = name;
        var url = url;
        var clicks = 0;

        return {

            inClicks: function(){
                clicks += 1;
                return clicks;
            },
            getClicks: function(){
                return clicks;
            },
            getName: function(){
                return name;
            },
            getUrl: function(){
                return url;
            }
        };
    };

    var alfred = new catPremium("Alfred", "http://placekitten.com/g/500/500");
    var victor = new catPremium("Victor", "http://placekitten.com/g/500/500");
    var cooper = new catPremium("Cooper", "http://placekitten.com/g/500/500");
    var leo = new catPremium("Leo", "http://placekitten.com/g/500/500");
    var piku = new catPremium("Piku", "http://placekitten.com/g/500/500");

    var catsPremium = [];
    catsPremium.push(alfred);
    catsPremium.push(victor);
    catsPremium.push(cooper);
    catsPremium.push(leo);
    catsPremium.push(piku);
    var containerpremium = $(".cat-container-premium");

    for(var i = 0; i < catsPremium.length; i++){

        var currentEl = catsPremium[i];
        $(containerpremium).append("<div class='cat-premium' id = '"+ currentEl.getName() +"'><img src='"+ currentEl.getUrl() +"' class='kittenClass' id= '"+i+"'><p id='clicks'>"+ currentEl.getClicks() +" clicks</p></div>");
    }

    $(".cat-premium").click(function(e){

        var el = e.target.parentElement;
        var id = el.childNodes[0].id;
        catsPremium[id].inClicks();
        $(el.childNodes[1]).html(catsPremium[id].getClicks() + " Clicks");
    });
})