
$("#id_wilaya").change(function () {
  var url = $("#personForm").attr("data-communes-url");
  var wilayaId = $(this).val();

  $.ajax({
    url: url,
    data: {
      'wilaya': wilayaId
    },
    success: function (data) {
      $("#id_commune").html(data);
    }
  });
});
$("#id_categorie").change(function () {
  var url = $("#personForm").attr("data-specialites-url");
  var categorieId = $(this).val();
  $.ajax({
    url: url,
    data: {
      'categorie': categorieId
    },
    success: function (data) {
       $("#id_specialite").html(data);
       $("#id_specialite").trigger("chosen:updated");
       $("#id_specialite").chosen();
    }
  });
});

$(window).ready(function () {
    $("#id_commune, #id_specialite").fadeOut();
    $("#id_commune, #id_specialite").siblings().fadeOut();
    $("#id_wilaya").find('option').click(function () {
        $("#id_commune").slideDown(500).siblings().slideDown(500);
    });
    $("#id_categorie").find('option').click(function () {
        $("#id_specialite").slideDown().siblings().slideDown();
        $("#id_specialite").fadeOut();
    });

    // Hide Placeholder On focus & Restore On Blur
    var placeAttr = '';
    $("[placeholder]").focus(function () {
        placeAttr = $(this).attr('placeholder');
        $(this).attr('placeholder', '');
        $(this).addClass("input-focus");

    }).blur(function () {
        $(this).attr('placeholder', placeAttr);
        $(this).removeClass("input-focus");
    })
});