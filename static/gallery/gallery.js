document.addEventListener("DOMContentLoaded", function (){
    const modal = document.getElementById("modal");
    const modalImg = document.getElementById("full-size-image");
    const close = document.querySelector(".close")
    const infoButton = document.querySelector(".display-info");
    const infoDiv = document.getElementById("image-info");

    let i = 0;
    let is_animate = false;
      
    //Function for updating image when using slider
    function updateImage(direction){
        //Prevents multiple clicks during transition
        if(is_animate) return;
        is_animate = true;

        const prev = document.querySelector('.prev_img');
        const current = document.querySelector('.current_img');
        const next = document.querySelector('.next_img');

        prev.style.transition = "transform 1s ease-in-out, opacity 1s ease-in-out";
        current.style.transition = "transform 1s ease-in-out, opacity 1s ease-in-out";
        next.style.transition = "transform 1s ease-in-out, opacity 1s ease-in-out";

        //When the direction changes, apply a fade effect to the
        //current image, and increase/decrease opacity for the
        //previous/next image
        if(direction === "next"){
            next.style.zIndex = "3";
            prev.style.zIndex = "1";

            prev.style.transform = "translateX(-240%) scale(0.8)";
            prev.style.opacity = "0.5";

            current.style.transform = "translateX(-100%) scale(0.9)";
            current.style.opacity = "0.7";

            next.style.transform = "translateX(0) scale(1)";
            next.style.opacity = "1";
            
        }
        else {
            prev.style.zIndex = "3";
            next.style.zIndex = "1";
        
            prev.style.transform = "translateX(0) scale(1)";
            prev.style.opacity = "1";

            current.style.transform = "translateX(100%) scale(0.9)";
            current.style.opacity = "0.7";

            next.style.transform = "translateX(240%) scale(0.8)";
            next.style.opacity = "0.5";
        }

        //Transition delay
        setTimeout(() => {
            if(direction === "next"){
                i = (i + 1) % images.length;
            }
            else {
                i = (i - 1 + images.length) % images.length;
            }

            prev.src = images[(i - 1 + images.length) % images.length];
            current.src = images[i];
            next.src = images[(i + 1) % images.length];

            //Reset the position after transition
            prev.style.transition = "none";
            current.style.transition = "none";
            next.style.transition = "none";

            prev.style.transform = "translateX(-100%) scale(0.9)";
            prev.style.opacity = "0.7";
            prev.style.zIndex = "1";

            current.style.transform = "translateX(0) scale(1)";
            current.style.opacity = "1";
            current.style.zIndex = "3";

            next.style.transform = "translateX(100%) scale(0.9)";
            next.style.opacity = "0.7";
            next.style.zIndex = "1";

            is_animate = false;
        }, 1000);
    }

    function nextImage() {
        updateImage("next");
    }

    function prevImage() {
        updateImage("prev");
    }

    //Toggle image info
    infoButton.addEventListener("click", function (){
        //Hide info if it's already displayed and
        //user clicks on the button
        if(infoDiv.style.display === "block"){
            infoDiv.style.display = "none";
        }
        else {
            infoDiv.style.display = "block";
        }
    })

    setTimeout(() => {
        const images = document.querySelectorAll(".current_img");

        //For full-sized image modal
        images.forEach(img => {
            img.addEventListener("click", function () {
                modal.style.display = "flex";
                modalImg.src = img.src;
            });
        });
        
    }, 500);

    //Close button for modal
    close.addEventListener("click", function (){
        modal.style.display = "none";
    });

    //Click anywhere on screen to close modal
    modal.addEventListener("click", function (e){
        if(e.target === modal){
            modal.style.display = "none";
        }
    });

    document.querySelector('.left').addEventListener('click', prevImage);
    document.querySelector('.right').addEventListener('click', nextImage);
});