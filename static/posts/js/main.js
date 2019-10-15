$(function () {
    $('#notify').delay(2500).hide(400);
});


$(function(){
    $('.drop').on('click', function(){
        $('.ellipsis').toggle()
    });
});


$(function () {
    $('.close').click(function () {
        $('.ad').css('display', 'none');
    })
})

var slimVid = document.getElementById('vid');
//intialize the magic controller
var controller = new ScrollMagic.Controller();

//build scene
var scene = new ScrollMagic.Scene({triggerElement:"#vid", duration:300})
  .addTo(controller)
  

  .on("enter", function(){
    slimVid.play();
  })

  .on("leave", function(){
    slimVid.pause();
  })


  $(document).ready(function(){
      $('#mytext').emojioneArea({
          pickerPosition:'bottom'
      });
  })


