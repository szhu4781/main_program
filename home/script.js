// Function for redirecting to the gallery page
function redirect(){
    window.location.href="gallery/gallery.html";
}

document.addEventListener("DOMContentLoaded", function (){
    const sections = ["main_body", "about", "footer"];
    let i = 0;
    const scrollButton = document.getElementById("scroll");
    const scrollIcon = document.getElementById("scroll-icon");

    // Function for scroll button
    scrollButton.addEventListener("click", function (){
        if(i < sections.length){
            document.getElementById(sections[i]).scrollIntoView({behavior: "smooth"});
            i++;
            
            // Check if the last section has been reached
            // if it's reached, then change arrow to up
            if(i === sections.length){
                scrollIcon.src = "../images/up-arrow.png";
            }
        }
        else {
            i = 0;  // Goes back to the top of the page
            window.scrollTo({top: 0, behavior: "smooth"});
            scrollIcon.src = "images/down-arrow.png";
        }
    });
});