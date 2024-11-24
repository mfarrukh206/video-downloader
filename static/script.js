document.getElementById("paste-url").addEventListener("click", () => {
    navigator.clipboard.readText().then((text) => {
        const textarea = document.getElementById("video-url");
        textarea.value += text + "\n";
    }).catch(err => console.error("Failed to read clipboard contents: ", err));
});

document.getElementById("clear").addEventListener("click", () => {
    document.getElementById("video-url").value = "";
});

document.getElementById("download-video").addEventListener("click", () => {
    const url = document.getElementById("video-url").value.trim();
    const quality = document.getElementById("quality").value;
    const status = document.getElementById("status");

    if (!url) {
        status.textContent = "Please enter a video URL.";
        return;
    }

    status.textContent = "Downloading... Please wait.";

    fetch('/download', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ url: url, quality: quality })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            status.textContent = "Error: " + data.error;
        } else {
            status.textContent = "Download ready!";
            const downloadLink = document.createElement("a");
            downloadLink.href = `/fetch-file/${data.file_path}`;
            downloadLink.download = '';
            downloadLink.textContent = "Click here to download your video";
            status.appendChild(document.createElement("br"));
            status.appendChild(downloadLink);
        }
    })
    .catch(error => {
        console.error("Error:", error);
        status.textContent = "An error occurred during download.";
    });
});
