var openSideNav = false;

$(document).ready(function () {
  $("#record").click(function () {
    $("#modal").removeClass("hidden");
  });

  $("#stop-recording").click(function () {
    $("#modal").addClass("hidden");
  });
});

function toggleSideNav() {
  openSideNav = !openSideNav;
  if (openSideNav) {
    $("#side-nav").addClass("open");
  } else {
    $("#side-nav").removeClass("open");
  }
}

