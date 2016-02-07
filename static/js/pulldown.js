$(".pulldown-toggle").click(function () {
  var pulldown = $(this).next('.pulldown');
  var chevron = $(this).children("i");

  if (pulldown.is(':visible')) {
    pulldown.slideUp();
    chevron.removeClass("fa-chevron-up").addClass("fa-chevron-down");
  } else {
    pulldown.slideDown();
    chevron.removeClass("fa-chevron-down").addClass("fa-chevron-up");
  }
});

$(".pulldown-close").click(function () {
  var pulldown = $(this).parent(".pulldown");
  var chevron = $(this).parent().prev(".pulldown-toggle").children("i");

  pulldown.slideUp();
  chevron.removeClass("fa-chevron-up").addClass("fa-chevron-down");

});