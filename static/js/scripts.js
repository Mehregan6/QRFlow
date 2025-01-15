document.getElementById('qr-form').addEventListener('input', function () {
    const formData = new FormData(this);
    fetch('/generate', {
        method: 'POST',
        body: formData
    })
    .then(response => response.blob())
    .then(blob => {
        const imageUrl = URL.createObjectURL(blob);
        document.getElementById('qr-image').src = imageUrl;
        document.getElementById('download-link').href = imageUrl;
    });
});