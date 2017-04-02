
function loadData() {

    var $body = $('body');
    var $wikiElem = $('#wikipedia-links');
    var $nytHeaderElem = $('#nytimes-header');
    var $nytElem = $('#nytimes-articles');
    var $greeting = $('#greeting');
    var newsEl = $('.news-container');

    // clear out old data before new request
    $wikiElem.text("");
    $nytElem.text("");

    var street = $("#street").val();
    var city = $("#city").val();
    var address = street + ", " + city;
    var url = 'http://maps.googleapis.com/maps/api/streetview?size=600x300&location=' + address + '';

    $body.append('<img class="bgimg" src="' + url + '">')

    var url = 'https://api.nytimes.com/svc/search/v2/articlesearch.json?q=' + city + '&sort=newest&api-key=217aad3291e84b0580a3766f6c68616d';
    console.log(url);
    $.ajax({
        url: url,
        method: 'GET',
        dataType: 'json',
        success: function(result){
            var news = result['response']['docs'];
            for(var i = 0; i < news.length; i++){

                var obj = news[i];
                var headline = obj['headline']['main'];
                var mainPara = obj['lead_paragraph']

                var element = "<div class='news-item'><h1>"+ headline +"</h1><br><p>"+ mainPara +"</p></div>";
                $(newsEl).append(element);
            }
        },
        error: function(){

            var element = "Sorry, the items could not be loaded!!!";
            $(newsEl).append(element);
        },
    });

    return false;
};

$('#form-container').submit(loadData);
