

const fileInput = document.getElementById("file-input");
const preview = document.getElementById("preview");
const applyBtn = document.getElementById("apply-btn");
const textInput = document.getElementById("text-input");

fileInput.addEventListener("change", () => {
    const file = fileInput.files[0];
    if (file) {
        preview.src = URL.createObjectURL(file);
        // Using classList to reveal it since Bootstrap uses 'd-none' 
        preview.classList.remove("d-none"); 
        preview.style.display = "block";
    }
});

applyBtn.addEventListener("click", async () => {
    const file = fileInput.files[0];
    const text = textInput.value;

    if (!file) {
        alert("Please select an image first!");
        return;
    }

    const formData = new FormData();
    formData.append("image", file);
    formData.append("text", text);

    const response = await fetch("/watermark", {
        method: "POST",
        body: formData
    });

    const blob = await response.blob();
    const url = URL.createObjectURL(blob);

    // Dynamic Filename Generation
    const originalName = file.name;
    const lastDot = originalName.lastIndexOf(".");
    
    let newFilename;
    if (lastDot !== -1) {
        // Splits "photo.jpg" into "photo" and ".jpg"
        const nameWithoutExt = originalName.substring(0, lastDot);
        const ext = originalName.substring(lastDot);
        newFilename = `${nameWithoutExt}_wm${ext}`;
    } else {
        // Fallback case if file has no extension
        newFilename = `${originalName}_wm.jpg`;
    }

    // Trigger the browser download
    const a = document.createElement("a");
    a.href = url;
    a.download = newFilename; // Uses the dynamic string we created above
    document.body.appendChild(a); // Temporarily append to DOM for compatibility
    a.click();
    a.remove(); // Clean up the DOM element
});