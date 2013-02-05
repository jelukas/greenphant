$(document).on("ready",confirms);

function confirms()
{
   $(".delete-subject").on("click",confirm_delete_subject); // is on base.html
   $(".delete-lesson").on("click",confirm_delete_lesson); // is on base.html
}