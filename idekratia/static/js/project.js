/* Project specific Javascript goes here. */


$(".alert")
	.fadeTo(2000, 500)
	.slideDown(500, function(){
    	$(".alert").alert('close');
	})
;
