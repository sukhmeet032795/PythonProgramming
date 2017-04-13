$(document).ready(function() {

    var Cat = function(){

        this.name = ko.observable("Tommy");
        this.imgSrc = ko.observable("http://placekitten.com/g/500/600");
        this.clickCount = ko.observable(0);
        this.imgAttr = ko.observable("Cute Cat");
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
        this.currentCat = ko.observable( new Cat() );

        this.incrementCount = function(){
            self.currentCat().clickCount( self.currentCat().clickCount() + 1 );
        }
    };

    ko.applyBindings(new viewFunction());
});