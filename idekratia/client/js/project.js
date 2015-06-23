/* Project specific Javascript goes here. */


$(".alert.messages")
	.fadeTo(2000, 500)
	.slideUp(500, function(){
    	$(".alert.messages").alert('close');
	})
;
