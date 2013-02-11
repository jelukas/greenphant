$(document).on('ready',document_ready);

var myPlayer = null;
_V_("video_course").ready(function(){

    myPlayer = this;    // Store the video object
    var aspectRatio = 9/16; // Make up an aspect ratio

    function resizeVideoJS(){
        // Get the parent element's actual width
        var width = document.getElementById(myPlayer.id).parentElement.offsetWidth;
        // Set width to fill parent element, Set height
        myPlayer.width(width).height( width * aspectRatio );
    }

    resizeVideoJS(); // Initialize the function
    window.onresize = resizeVideoJS; // Call the function on resize
});

function document_ready(){
    $('#freeVideo').on('hidden', function () {
        myPlayer.pause();
    });

    // Remove the options form modal to allow call another data-remote url
    $('body').on('hidden', '.modal', function () {
        $(this).removeData('modal');
    });
}

