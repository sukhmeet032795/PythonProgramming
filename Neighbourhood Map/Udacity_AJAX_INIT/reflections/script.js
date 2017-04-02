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
    console.log(cats)

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
})