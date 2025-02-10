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
        if (selectedFiles.length === 0) {
            alert("No files selected.");
            event.preventDefault();
            return;
        }

        const userConfirmed = confirm("Are you sure you want to upload these images? They can be viewed by anyone at any given time.");
        if (!userConfirmed) {
            event.preventDefault();
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
        .then(response => response.text())
        .then(data => {
            alert("Upload successful!");
            window.location.href = "/gallery";
        })
        .catch(error => {
            alert("Upload failed. Try again.");
        });

        event.preventDefault();
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
});
