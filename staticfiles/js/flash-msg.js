$(document).ready(function() {
  console.log('ok2')
})

function showFlashMessage() {
  $(".container-alert-flash").fadeIn();
  setTimeout(function(){
            $(".container-alert-flash").fadeOut();
  },1000)
}
