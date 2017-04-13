$(document).ready(function() {

    var instancesCat= [
        {
            clickCount : 0,
            name : 'Tabby',
            imgSrc : 'img/434164568_fea0ad4013_z.jpg',
            imgAttribution : 'https://www.flickr.com/photos/bigtallguy/434164568'
        },
        {
            clickCount : 0,
            name : 'Tiger',
            imgSrc : 'img/4154543904_6e2428c421_z.jpg',
            imgAttribution : 'https://www.flickr.com/photos/xshamx/4154543904'
        },
        {
            clickCount : 0,
            name : 'Scaredy',
            imgSrc : 'img/22252709_010df3379e_z.jpg',
            imgAttribution : 'https://www.flickr.com/photos/kpjas/22252709'
        },
        {
            clickCount : 0,
            name : 'Shadow',
            imgSrc : 'img/1413379559_412a540d29_z.jpg',
            imgAttribution : 'https://www.flickr.com/photos/malfet/1413379559'
        },
        {
            clickCount : 0,
            name : 'Sleepy',
            imgSrc : 'img/9648464288_2516b35537_z.jpg',
            imgAttribution : 'https://www.flickr.com/photos/onesharp/9648464288'
        }
    ];

    var Cat = function(data){

        this.name = ko.observable(data.name);
        this.imgSrc = ko.observable(data.imgSrc);
        this.clickCount = ko.observable(data.clickCount);
        this.imgAttr = ko.observable(data.imgAttribution);
        this.nicknames = ko.observableArray(['Leo', 'Piku', 'Larry'])

        this.title = ko.computed(function(){

            var title;
            var clicks = this.clickCount();

            if(clicks < 10){
                title = 'Newborn';
            }
            else if(clicks < 50){
                title = 'Infant';
            }
            else if(clicks < 100){
                title = 'Child';
            }
            else if(clicks < 200){
                title = 'Teen';
            }
            else if(clicks < 500){
                title = 'Adult';
            }
            else{
                title = 'Ninja';
            }

            return title;
        }, this);
    };

    var viewFunction = function(){

        var self = this;

        this.cats = ko.observableArray([]);

        instancesCat.forEach(function(cat){
            self.cats.push( new Cat(cat) );
        });

        self.currentCat = ko.observable( self.cats()[0] );

        var listEl = $("#catList");

        self.cats().forEach(function(cat){

            el = document.createElement('li');
            el.textContent = cat.name();

            $(el).click((function(cat){
                return function(){
                    self.currentCat(cat);
                }
            })(cat));

            $(listEl).append(el);
        });

        this.incrementCount = function(){
            self.currentCat().clickCount( self.currentCat().clickCount() + 1 );
        }
    };

    ko.applyBindings(new viewFunction());
});