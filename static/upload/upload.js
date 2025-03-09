document.addEventListener('DOMContentLoaded', function () {
    const uploadForm = document.querySelector("form");
    const fileInput = document.getElementById("file-input");
    const fileName = document.getElementById("file-name");
    const contain = document.getElementById("upload-container");

    let selectedFiles = [];

    // Updates the list of uploaded files
    fileInput.addEventListener('change', function () {
        selectedFiles = Array.from(fileInput.files);
        updateDisplay();
    });

    // Drag and drop events
    contain.addEventListener("dragover", function (event) {
        event.preventDefault();
        contain.style.border = "8px solid rgb(120, 120, 120)";
    });

    contain.addEventListener("dragleave", function (event) {
        event.preventDefault();
        contain.style.border = "8px dashed rgb(167, 167, 167)";
    });

    contain.addEventListener("drop", function (event) {
        event.preventDefault();
        contain.style.border = "8px solid rgb(167, 167, 167)";

        let droppedFiles = Array.from(event.dataTransfer.files);
        selectedFiles = selectedFiles.concat(droppedFiles);

        let dataTransfer = new DataTransfer();
        selectedFiles.forEach(file => dataTransfer.items.add(file));
        fileInput.files = dataTransfer.files; // This updates the input field
        
        updateDisplay();
    });

    // Confirmation for upload
    uploadForm.addEventListener("submit", function (event) {
        event.preventDefault();

        if (selectedFiles.length === 0) {
            alert("No files selected.");
            return;
        }

        const userConfirmed = confirm("Are you sure you want to upload these images? They can be viewed by anyone at any given time.");
        if (!userConfirmed) {
            return;
        }

        let formData = new FormData();
        selectedFiles.forEach(file => {
            formData.append("files", file);  // Correctly append all files
        });

        fetch("/upload", {
            method: "POST",
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if(data.status === "error"){
                alert(data.message);
            } else if (data.status === "success"){
                alert(data.message);
                window.location.href = "/gallery";
            }
        })
        .catch(error => {
            alert("Upload failed. Try again.");
        });
    });

    // Function for updating the display of files chosen
    function updateDisplay() {
        if (selectedFiles.length > 0) {
            let fileList = selectedFiles.map(file => file.name).join(', ');
            fileName.textContent = `Selected files: ${fileList}`;
            fileName.style.display = 'block';
        } else {
            fileName.textContent = `No file selected.`;
            fileName.style.display = 'none';
        }
    }

    //Fetch the microservice host
    const toggleButton = document.getElementById('mode-toggle');
    fetch("http://localhost:5001/mode")
        .then(response => response.json())
        .then(data => {
            const userMode = data.mode;
            applyTheme(userMode);
        })
        .catch(error => console.error('error fetching theme:', error));
    
    //Button for toggling theme
    toggleButton.addEventListener("click", function(){
    let current_theme;

        //If the body has class dark-mode, switch to light mode
        if(document.body.classList.contains("dark-mode")){
            current_theme = "light";
        } else {
            current_theme = "dark";
        }

        applyTheme(current_theme);

        //Save preference to microservice
        fetch("http://localhost:5001/mode", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ mode: current_theme }),
        })
        .then(response => response.json())
        .then(data => console.log(data.message))
        .catch(error => console.error("error setting theme", error));
    });
});

const modeLabel = document.querySelector('.mode-label');

//Function for applying web app theme
function applyTheme(mode){
    //Check if theme is dark or light, remove and replace
    //the corresponding one
    if(mode === "dark"){
        document.body.classList.add("dark-mode");
        document.body.classList.remove("light-mode");
        modeLabel.textContent = "Dark";
    } else {
        document.body.classList.add("light-mode");
        document.body.classList.remove("dark-mode");
        modeLabel.textContent = "Light";
    }
}
