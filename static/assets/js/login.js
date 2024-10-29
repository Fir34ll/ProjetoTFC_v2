$(document).ready(function() {
    function isMobile() {
        return window.innerWidth <= 768;
    }

    $("#signup_btn").click(function() {
        if (isMobile()) {
            $("#loginform").addClass('slide-up');
            $("#signupform").addClass('slide-up').css('visibility', 'visible');
            $("#login_msg").fadeOut(300);
            $("#signup_msg").fadeIn(300);
            $("#main").css('height', '450px'); // Altura aumentada para acomodar o formulário de registro
        } else {
            // Impede que múltiplas animações se sobreponham
            $("#main, #loginform, #signupform").stop(true, true);

            // Move o #main para a posição da página de registro
            $("#main").animate({left: "22.5%"}, 100).animate({left: "30%"}, 200);

            // Esconde o #loginform
            $("#loginform").css("visibility", "hidden").animate({left: "25%"}, 400);

            // Move e mostra o #signupform
            $("#signupform").css("visibility", "visible").css("left", "17%").animate({left: "30%"}, 300);
        }
    });

    $("#login_btn").click(function() {
        if (isMobile()) {
            $("#loginform").removeClass('slide-up');
            $("#signupform").removeClass('slide-up');
            $("#signup_msg").fadeOut(300);
            $("#login_msg").fadeIn(300);
            $("#main").css('height', '400px'); // Retorna à altura original
        } else {
            // Impede que múltiplas animações se sobreponham
            $("#main, #loginform, #signupform").stop(true, true);

            // Move o #main para a posição da página de login
            $("#main").animate({left: "77.5%"}, 100).animate({left: "70%"}, 200);

            // Esconde o #signupform
            $("#signupform").css("visibility", "hidden").animate({left: "75%"}, 400);

            // Move e mostra o #loginform
            $("#loginform").css("visibility", "visible").css("left", "83.5%").animate({left: "70%"}, 300);
        }
    });
});
