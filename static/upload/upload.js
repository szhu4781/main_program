document.addEventListener('DOMContentLoaded', function () {
    const uploadForm = document.querySelector("form");
    const fileInput = document.getElementById("file-input");
    const fileName = document.getElementById("file-name");

    fileInput.addEventListener('change', function (){
        const files = fileInput.files;
        if(files.length > 0){
            let selectedFiles = Array.from(files).map(file => file.name).join(', ')
            fileName.textContent = `Selected files: ${selectedFiles}`;
            fileName.style.display = 'block';
        } else {
            fileName.textContent = `No file selected.`;
            fileName.style.display = 'none';
        }
    });

    uploadForm.addEventListener("submit", function (event){
        const userConfirmed = confirm("Are you sure you want to upload this image? Your image can be viewed by anyone at any given time.");

        if(!userConfirmed){
            event.preventDefault();
        }
    });
});