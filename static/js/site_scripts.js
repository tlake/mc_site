// ################
// PULLDOWN
// ################

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


// ################
// AJAX
// ################

function makeQuery (address, port) {
  return $.ajax({
    type: "GET",
    url: "/query",
    data: {
      "address": address,
      "port": port,
    },
  })
};

function queryServers (servers) {
  $.find(".server").each(function () {
    var locInfo = $(this).(".location > span").text().split(":");
    makeQuery(locInfo[0], locInfo[1]).done(function (response) {
      var playersList = [];
      for (name in response.player_names) {
        playersList.push("<li>" + name + "</li>")
      };
      $(this).find(".status > span").html(response.status);
      $(this).find(".players-summary").html(
        response.players_online + "/" + response.players_max
      );
      $(this).find("ul").html(playersList);
    });
  })
};