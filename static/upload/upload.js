document.addEventListener('DOMContentLoaded', function () {
    const uploadForm = document.querySelector("form");
    const fileInput = document.getElementById("file-input");
    const fileName = document.getElementById("file-name");
    const contain = document.getElementById("upload-container");

    //Updates the list of uploaded files
    fileInput.addEventListener('change', function (){
        updateDisplay(fileInput.files);
        
    });

    //Drag and drop events
    contain.addEventListener("dragover", function (event){
        event.preventDefault();
        contain.style.border = "8px solid rgb(120, 120, 120)";
    });

    contain.addEventListener("dragleave", function (event){
        event.preventDefault();
        contain.style.border = "8px dashed rgb(167, 167, 167)";
    });

    contain.addEventListener("drop", function (event){
        event.preventDefault();
        contain.style.border = "8px solid rgb(167, 167, 167)";

        const files = event.dataTransfer.files;
        fileInput.files = files;
        updateDisplay(files);
    });

    //Confirmation for upload
    uploadForm.addEventListener("submit", function (event){
        const userConfirmed = confirm("Are you sure you want to upload this image? Your image can be viewed by anyone at any given time.");

        if(!userConfirmed){
            event.preventDefault();
        }
    });

    //Function for updating the display of files chosen
    function updateDisplay(files){
        if(files.length > 0){
            let selectedFiles = Array.from(files).map(file => file.name).join(', ')
            fileName.textContent = `Selected files: ${selectedFiles}`;
            fileName.style.display = 'block';
        } else {
            fileName.textContent = `No file selected.`;
            fileName.style.display = 'none';
        }
    }
});