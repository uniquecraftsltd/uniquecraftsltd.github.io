(function ($) {
    "use strict";

    // Initiate the wowjs
    new WOW().init();

    // Back to top button
    $(window).scroll(function () {
        if ($(this).scrollTop() > 200) {
            $('.back-to-top').fadeIn('slow');
        } else {
            $('.back-to-top').fadeOut('slow');
        }
    });
    $('.back-to-top').click(function () {
        $('html, body').animate({scrollTop: 0}, 1500, 'easeInOutExpo');
        return false;
    });

    // Sticky Navbar
    $(window).scroll(function () {
        if ($(this).scrollTop() > 90) {
            $('.nav-bar').addClass('nav-sticky');
            $('.carousel, .page-header').css("margin-top", "73px");
        } else {
            $('.nav-bar').removeClass('nav-sticky');
            $('.carousel, .page-header').css("margin-top", "0");
        }
    });

    // Dropdown on mouse hover
    $(document).ready(function () {
        function toggleNavbarMethod() {
            if ($(window).width() > 992) {
                $('.navbar .dropdown').on('mouseover', function () {
                    $('.dropdown-toggle', this).trigger('click');
                }).on('mouseout', function () {
                    $('.dropdown-toggle', this).trigger('click').blur();
                });
            } else {
                $('.navbar .dropdown').off('mouseover').off('mouseout');
            }
        }
        toggleNavbarMethod();
        $(window).resize(toggleNavbarMethod);
    });

    // jQuery counterUp
    $('[data-toggle="counter-up"]').counterUp({
        delay: 10,
        time: 2000
    });

    // Modal Video
    $(document).ready(function () {
        var $videoSrc;

        $('.btn-play').click(function () {
            $videoSrc = $(this).data("src");
        });

        $('#videoModal').on('shown.bs.modal', function (e) {
            // اضافه کردن پارامترهای پخش خودکار به انتهای لینک
            $("#video").attr('src', $videoSrc + "?autoplay=1&rel=0&modestbranding=1");
        });

        $('#videoModal').on('hide.bs.modal', function (e) {
            // خالی کردن منبع برای توقف کامل ویدیو هنگام بستن
            $("#video").attr('src', '');
        });
    });
    

    // Testimonial Slider
    $('.testimonial-slider').slick({
        infinite: true,
        autoplay: true,
        arrows: false,
        dots: false,
        slidesToShow: 1,
        slidesToScroll: 1,
        asNavFor: '.testimonial-slider-nav'
    });
    $('.testimonial-slider-nav').slick({
        arrows: false,
        dots: false,
        focusOnSelect: true,
        centerMode: true,
        centerPadding: '22px',
        slidesToShow: 3,
        asNavFor: '.testimonial-slider'
    });
    $('.testimonial .slider-nav').css({"position": "relative", "height": "160px"});

    // Blogs carousel
    $(".related-slider").owlCarousel({
        autoplay: true,
        dots: false,
        loop: true,
        nav : true,
        navText : [
            '<i class="fa fa-angle-left" aria-hidden="true"></i>',
            '<i class="fa fa-angle-right" aria-hidden="true"></i>'
        ],
        responsive: {
            0:{ items:1 },
            576:{ items:1 },
            768:{ items:2 }
        }
    });

    // Portfolio Dynamic Loader (Updated for Multi-Project SAPE)
    $(document).ready(function () {
        const galleryContainer = $('.portfolio-container');

        fetch('img/projects/global_manifest.json')
            .then(response => response.json())
            .then(projects => {
                projects.forEach(project => {
                    // برای هر پروژه، تصاویرش را به گالری اضافه می‌کنیم
                    project.gallery.forEach(imgUrl => {
                        const item = `
                            <div class="col-lg-4 col-md-6 col-sm-12 portfolio-item filter-${project.id} wow fadeInUp" data-wow-delay="0.1s">
                                <div class="portfolio-warp">
                                    <div class="portfolio-img">
                                        <img src="${imgUrl}" alt="${project.title}">
                                        <div class="portfolio-overlay">
                                            <p>${project.title}</p>
                                        </div>
                                    </div>
                                    <div class="portfolio-text">
                                        <h3>${project.title}</h3>
                                        <a class="btn" href="${imgUrl}" data-lightbox="portfolio">+</a>
                                    </div>
                                </div>
                            </div>`;
                        galleryContainer.append(item);
                    });
                });

                // Re-initialize Isotope
                const portfolioIsotope = galleryContainer.isotope({
                    itemSelector: '.portfolio-item',
                    layoutMode: 'fitRows'
                });

                // تنظیم فیلترها (بر اساس ID پروژه)
                $('#portfolio-flters li').on('click', function () {
                    $("#portfolio-flters li").removeClass('filter-active');
                    $(this).addClass('filter-active');
                    portfolioIsotope.isotope({filter: $(this).data('filter')});
                });
            })
            .catch(err => console.error("Error loading portfolio:", err));
    });

