$(document).ready((event) => {
  $(".btn").click((event) => {
    $("#scrapping-result").html("Loading...");
    $(".btn").addClass("disabled");
  });
  $("#pills-home-tab").click((event) => {
    $("#company-scrapping-result").hide();
    $("#pubmed-scrapping-result").show();
    $("#rxcist-scrapping-result").show();
  });
  $("#pills-profile-tab").click((event) => {
    $("#company-scrapping-result").show();
    $("#pubmed-scrapping-result").hide();
    $("#rxcist-scrapping-result").hide();
  });
});
