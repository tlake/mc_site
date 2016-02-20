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

function queryServers () {
  $(".server").each(function () {
    var elem = $(this);
    var locInfo = elem.find(".location > span").text().split(":");
    makeQuery(locInfo[0], locInfo[1]).done(function (response) {
      names = response.player_names;
      var playersList = "";
      for (var i = 0; i < names.length; i++) {
        playersList = playersList + "<li>" + names[i] + "</li>";
      }
      elem.find(".status > span").html(response.status);
      elem.find(".players-summary").html(
        response.players_online + "/" + response.players_max + " Players"
      );
      if (playersList) {
        elem.find("ul").html(playersList);
      } else {
        elem.find("ul").html("");
      }
    })
  })
};


// ################
// READY
// ################

$(function () {
  setInterval(queryServers, 5000);
});