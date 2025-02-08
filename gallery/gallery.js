document.addEventListener("DOMContentLoaded", function (){
    const images = ["../images/1.jpg", "../images/2.jpg", "../images/3.jpg"];
    let i = 0;

    function updateImage(){
        const prev = document.querySelector('.prev_img');
        const current = document.querySelector('.current_img');
        const next = document.querySelector('.next_img');

        prev.src = images[(i - 1 + images.length) % images.length];
        current.src = images[i];
        next.src = images[(i + 1) % images.length];

        prev.style.transform = "translateX(-120%)";
        current.style.transform = "translateX(0)";
        next.style.transform = "translateX(120%)";
    }

    function nextImage(){
        i = (i + 1) % images.length;
        updateImage();
    }

    function prevImage(){
        i = (i - 1 + images.length) % images.length;
        updateImage();
    }

    document.querySelector('.left').addEventListener('click', prevImage);
    document.querySelector('.right').addEventListener('click', nextImage);

    updateImage();
});