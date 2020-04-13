$(document).on("turbolinks:load", function () {
  $(".btn").click((event) => {
    $(".btn").addClass("disabled");
  });
});
