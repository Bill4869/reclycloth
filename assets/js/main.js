/**
* Template Name: Squadfree - v2.3.1
* Template URL: https://bootstrapmade.com/squadfree-free-bootstrap-template-creative/
* Author: BootstrapMade.com
* License: https://bootstrapmade.com/license/
*/
// import {DrawingBoard} from "../drawingBoard/drawingboard.min.js";
!(function ($) {
  "use strict";

  //FastAPI
  var file = null;
  var blob = null;
  var blob1 = null;
  const RESIZED_WIDTH = 512;
  const RESIZED_HEIGHT = 512;

  $('input[name="userfile"]').change(function () {
    file = $(this).prop("files")[0];

    // ファイルチェック
    if (file.type != "image/jpeg" && file.type != "image/png") {
      file = null;
      blob = null;
      return;
    }

    var result = document.getElementById("result");
    result.innerHTML = "";

    // 画像をリサイズする
    var image = new Image();
    var reader = new FileReader();
    reader.onload = function (e) {
      image.onload = function () {
        var width, height;

        // 縦or横の長い方に合わせてリサイズする
        if (image.width > image.height) {
          var ratio = image.height / image.width;
          width = RESIZED_WIDTH;
          height = RESIZED_WIDTH * ratio;
        } else {
          var ratio = image.width / image.height;
          width = RESIZED_HEIGHT * ratio;
          height = RESIZED_HEIGHT;
        }

        var canvas = $("#canvas").attr("width", width).attr("height", height);
        var ctx = canvas[0].getContext("2d");
        ctx.clearRect(0, 0, width, height);
        ctx.drawImage(
          image,
          0,
          0,
          image.width,
          image.height,
          0,
          0,
          width,
          height
        );

        // canvasからbase64画像データを取得し、POST用のBlobを作成する
        var base64 = canvas.get(0).toDataURL("image/jpeg");
        var barr, bin, i, len;
        bin = atob(base64.split("base64,")[1]);
        len = bin.length;
        barr = new Uint8Array(len);
        i = 0;
        while (i < len) {
          barr[i] = bin.charCodeAt(i);
          i++;
        }
        blob = new Blob([barr], { type: "image/jpeg" });
        console.log(blob);
      };
      image.src = e.target.result;
    };
    reader.readAsDataURL(file);
  });


  $('input[name="userfile1"]').change(function () {
    file = $(this).prop("files")[0];

    // ファイルチェック
    if (file.type != "image/jpeg" && file.type != "image/png") {
      file = null;
      blob = null;
      return;
    }

    var result = document.getElementById("result");
    result.innerHTML = "";

    // 画像をリサイズする
    var image = new Image();
    var reader = new FileReader();
    reader.onload = function (e) {
      image.onload = function () {
        var width, height;

        // 縦or横の長い方に合わせてリサイズする
        if (image.width > image.height) {
          var ratio = image.height / image.width;
          width = RESIZED_WIDTH;
          height = RESIZED_WIDTH * ratio;
        } else {
          var ratio = image.width / image.height;
          width = RESIZED_HEIGHT * ratio;
          height = RESIZED_HEIGHT;
        }

        var canvas = $("#canvas1").attr("width", width).attr("height", height);
        var ctx = canvas[0].getContext("2d");
        ctx.clearRect(0, 0, width, height);
        ctx.drawImage(
          image,
          0,
          0,
          image.width,
          image.height,
          0,
          0,
          width,
          height
        );

        // canvasからbase64画像データを取得し、POST用のBlobを作成する
        var base64 = canvas.get(0).toDataURL("image/jpeg");
        var barr, bin, i, len;
        bin = atob(base64.split("base64,")[1]);
        len = bin.length;
        barr = new Uint8Array(len);
        i = 0;
        while (i < len) {
          barr[i] = bin.charCodeAt(i);
          i++;
        }
        blob1 = new Blob([barr], { type: "image/jpeg" });
        console.log(blob1);
      };
      image.src = e.target.result;
    };
    reader.readAsDataURL(file);
  });

  function ImageToBase64(img, mime_type) {
    // New Canvas
    var canvas = document.createElement('canvas');
    canvas.width = img.naturalWidth;
    canvas.height = img.naturalHeight;
    // Draw Image
    var ctx = canvas.getContext('2d');
    ctx.drawImage(img, 0, 0);
    // To Base64
    return canvas.toDataURL(mime_type);
  }
  

  document.getElementById("zbeubeu").style.display = "none";
  document.getElementById("draw").style.display = "none";
  $("#nav-sketch-tab").click(function () {
    document.getElementById("draw").style.display = "block";
    document.getElementById("zbeubeu").style.display = "none";
    document.getElementById("canvas").style.display = "block";
    document.getElementById("uploadSec").style.display = "block";

  });
  $("#nav-photo-tab").click(function () {
    document.getElementById("draw").style.display = "none";
    document.getElementById("zbeubeu").style.display = "none";
    document.getElementById("canvas").style.display = "block";
    document.getElementById("uploadSec").style.display = "block";
});
  $("#nav-design-tab").click(function () {
    document.getElementById("draw").style.display = "none";
    document.getElementById("zbeubeu").style.display = "block";
    document.getElementById("uploadSec").style.display = "none";
    document.getElementById("canvas").style.display = "none";

});
  
  // アップロード開始ボタンがクリックされたら
  $("#post").click(function () {
    if(document.getElementById("zbeubeu").style.display == "block") {
      var img = document.getElementById('zbeubeu').getElementsByClassName("drawing-board-canvas-wrapper")[0].getElementsByClassName("drawing-board-canvas")[0];
      var skg = img.toDataURL("image/png");
    }
    else {
      var img = document.getElementById('canvas');
      var skg = img.toDataURL("image/png");
      //var skg = ImageToBase64(img, "image/png");
    }
    
    var ele = document.getElementsByName('userfile1');
    for (var i = 0; i < ele.length; i++) {
      if (ele[i].checked)
        var x = ele[i].value;
    }

    var tab = document.getElementsByName('functab');
    // console.log(tab[0].ariaSelected);
    for (var i = 0; i < tab.length; i++) {
      if (tab[i].ariaSelected == "true")
        var tabid = tab[i].id;
    }

    var dr = document.getElementsByName('drawMethod');
    for (var i = 0; i < dr.length; i++) {
      if (dr[i].checked)
        var drawmeth = dr[i].value;
    }

    


    var img = document.getElementById(x);
    // console.log(img);
    var txt = ImageToBase64(img, "image/jpg");

    var json_asocc = { "skg": skg, "txt": txt }
    var json_text = JSON.stringify(json_asocc);

    var xhr = new XMLHttpRequest;       //インスタンス作成
    xhr.onload = function () {        //レスポンスを受け取った時の処理（非同期）
      var data = xhr.responseText;

      var response = JSON.parse(data);

      var result = document.getElementById("result");
      var data = "data:image/jpg;base64," + response["response"];

      var cvs = document.getElementById('cvs1');
      var ctx = cvs.getContext('2d');

      //画像オブジェクトを生成
      var img = new Image();
      img.src = data;

      //画像をcanvasに設定
      img.onload = function () {
        console.log(img.height,img.width);
        cvs.width=img.width;
        cvs.height=img.height;
        ctx.drawImage(img, 0, 0, img.width, img.height);
      }
    };
    xhr.onerror = function () {       //エラーが起きた時の処理（非同期）
      alert("error!");
    }


    if (tabid == "nav-photo-tab") {
      xhr.open('post', "http://127.0.0.1:8000/api/imgtoimg", true);

    }
    else if (tabid == "nav-sketch-tab") {
      if (drawmeth == "drclothes") {
        xhr.open('post', "http://127.0.0.1:8000/api/skechtoimg_cloth", true);
      }
      if (drawmeth == "drbags") {
        xhr.open('post', "http://127.0.0.1:8000/api/skechtoimg_bag", true);

      }
      if (drawmeth == "drshoes") {
        xhr.open('post', "http://127.0.0.1:8000/api/skechtoimg_shoes", true);
      }
    }
    else if (tabid == "nav-design-tab") {
      xhr.open('post', "http://127.0.0.1:8000/api/skechtoimg_cloth", true)
    }

    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(json_text);


  });


  //end API

  // Smooth scroll for the navigation menu and links with .scrollto classes
  var scrolltoOffset = $('#header').outerHeight() - 31;
  if (window.matchMedia("(max-width: 991px)").matches) {
    scrolltoOffset += 30;
  }
  $(document).on('click', '.nav-menu a, .mobile-nav a, .scrollto', function (e) {
    if (location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') && location.hostname == this.hostname) {
      var target = $(this.hash);
      e.preventDefault();
      if (target.length) {

        var scrollto = target.offset().top - scrolltoOffset;
        if ($(this).attr("href") == '#header') {
          scrollto = 0;
        }
        $('html, body').animate({
          scrollTop: scrollto
        }, 1500, 'easeInOutExpo');
        if ($(this).parents('.nav-menu, .mobile-nav').length) {
          $('.nav-menu .active, .mobile-nav .active').removeClass('active');
          $(this).closest('li').addClass('active');
        }
        if ($('body').hasClass('mobile-nav-active')) {
          $('body').removeClass('mobile-nav-active');
          $('.mobile-nav-toggle i').toggleClass('icofont-navigation-menu icofont-close');
          $('.mobile-nav-overly').fadeOut();
        }
        return false;
      }
    }
  });

  // Activate smooth scroll on page load with hash links in the url
  $(document).ready(function () {
    if (window.location.hash) {
      var initial_nav = window.location.hash;
      if ($(initial_nav).length) {
        var scrollto = $(initial_nav).offset().top - scrolltoOffset;
        $('html, body').animate({
          scrollTop: scrollto
        }, 1500, 'easeInOutExpo');
      }
    }
  });

  // Mobile Navigation
  if ($('.nav-menu').length) {
    var $mobile_nav = $('.nav-menu').clone().prop({
      class: 'mobile-nav d-lg-none'
    });
    $('body').append($mobile_nav);
    $('body').prepend('<button type="button" class="mobile-nav-toggle d-lg-none"><i class="icofont-navigation-menu"></i></button>');
    $('body').append('<div class="mobile-nav-overly"></div>');
    $(document).on('click', '.mobile-nav-toggle', function (e) {
      $('body').toggleClass('mobile-nav-active');
      $('.mobile-nav-toggle i').toggleClass('icofont-navigation-menu icofont-close');
      $('.mobile-nav-overly').toggle();
    });
    $(document).on('click', '.mobile-nav .drop-down > a', function (e) {
      e.preventDefault();
      $(this).next().slideToggle(300);
      $(this).parent().toggleClass('active');
    });
    $(document).click(function (e) {
      var container = $(".mobile-nav, .mobile-nav-toggle");
      if (!container.is(e.target) && container.has(e.target).length === 0) {
        if ($('body').hasClass('mobile-nav-active')) {
          $('body').removeClass('mobile-nav-active');
          $('.mobile-nav-toggle i').toggleClass('icofont-navigation-menu icofont-close');
          $('.mobile-nav-overly').fadeOut();
        }
      }
    });
  } else if ($(".mobile-nav, .mobile-nav-toggle").length) {
    $(".mobile-nav, .mobile-nav-toggle").hide();
  }

  // Navigation active state on scroll
  var nav_sections = $('section');
  var main_nav = $('.nav-menu, .mobile-nav');

  $(window).on('scroll', function () {
    var cur_pos = $(this).scrollTop() + 200;

    nav_sections.each(function () {
      var top = $(this).offset().top,
        bottom = top + $(this).outerHeight();

      if (cur_pos >= top && cur_pos <= bottom) {
        if (cur_pos <= bottom) {
          main_nav.find('li').removeClass('active');
        }
        main_nav.find('a[href="#' + $(this).attr('id') + '"]').parent('li').addClass('active');
      }
      if (cur_pos < 300) {
        $(".nav-menu ul:first li:first").addClass('active');
      }
    });
  });

  // Toggle .header-scrolled class to #header when page is scrolled
  $(window).scroll(function () {
    if ($(this).scrollTop() > 100) {
      $('#header').addClass('header-scrolled');
    } else {
      $('#header').removeClass('header-scrolled');
    }
  });
  if ($(window).scrollTop() > 100) {
    $('#header').addClass('header-scrolled');
  }

  //upload image with preview
  $(document).on("click", ".browse", function () {
    var file = $(this).parents().find(".file");
    file.trigger("click");
  });
  $('input[type="file"]').change(function (e) {
    var fileName = e.target.files[0].name;
    $("#file").val(fileName);

    var reader = new FileReader();
    reader.onload = function (e) {
      // get loaded data and render thumbnail.
      document.getElementById("preview").src = e.target.result;
    };
    // read the image file as a data URL.
    reader.readAsDataURL(this.files[0]);
  });

  // Back to top button
  $(window).scroll(function () {
    if ($(this).scrollTop() > 100) {
      $('.back-to-top').fadeIn('slow');
    } else {
      $('.back-to-top').fadeOut('slow');
    }
  });
  $('.back-to-top').click(function () {
    $('html, body').animate({
      scrollTop: 0
    }, 1500, 'easeInOutExpo');
    return false;
  });

  // jQuery counterUp
  $('[data-toggle="counter-up"]').counterUp({
    delay: 10,
    time: 1000
  });

  // Porfolio isotope and filter
  $(window).on('load', function () {
    var portfolioIsotope = $('.portfolio-container').isotope({
      itemSelector: '.portfolio-item',
      layoutMode: 'fitRows'
    });
    $('#portfolio-flters li').on('click', function () {
      $("#portfolio-flters li").removeClass('filter-active');
      $(this).addClass('filter-active');
      portfolioIsotope.isotope({
        filter: $(this).data('filter')
      });
      aos_init();
    });
  });

  // Initiate venobox (lightbox feature used in portofilo)
  $(document).ready(function () {
    $('.venobox').venobox();
  });

  // Testimonials carousel (uses the Owl Carousel library)
  $(".testimonials-carousel").owlCarousel({
    autoplay: true,
    dots: true,
    loop: true,
    responsive: {
      0: {
        items: 1
      },
      768: {
        items: 2
      },
      900: {
        items: 3
      }
    }
  });

  // Portfolio details carousel
  $(".portfolio-details-carousel").owlCarousel({
    autoplay: true,
    dots: true,
    loop: true,
    items: 1
  });

  // Init AOS
  function aos_init() {
    AOS.init({
      duration: 800,
      easing: "ease-in-out",
      once: true
    });
  }
  $(window).on('load', function () {
    aos_init();
  });

})(jQuery);