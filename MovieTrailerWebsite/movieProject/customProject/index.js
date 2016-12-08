$(function(){

	$('.trailerClass a').click(function(e){

		e.preventDefault();
		var current = $(this);
		var url = $(current).attr("id");
		var title = $(current).attr("name");

		$('.modal-content iframe').attr("src" , url);
		$('.modal-content p').text(title);

		$('#trailerModal').modal('open');
	});

	$('.modal').modal({

		dismissible: false, 
		opacity: .5, 
		in_duration: 300, 
		out_duration: 300, 
		starting_top: '4%', 
		ending_top: '10%'
	});

	$('.modal-close').click(function(e){

		$('#trailerModal').modal('close');
		$('.modal-content iframe').attr("src" , "");
		$('.modal-content p').text("");	
	});
});