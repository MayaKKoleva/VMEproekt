// static/js/script.js
document.getElementById('upload-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const formData = new FormData(this);
    
    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            console.error(data.error);
        } else {
            const gallery = document.getElementById('gallery');
            data.files.forEach(filename => {
                const imgContainer = document.createElement('div');
                imgContainer.className = 'image-container';

                const img = document.createElement('img');
                img.src = `/uploads/${filename}`;

                const deleteBtn = document.createElement('button');
                deleteBtn.innerHTML = '<i class="fas fa-trash"></i>';
                deleteBtn.className = 'delete-btn';
                deleteBtn.dataset.filename = filename; // Store the filename as a data attribute
                deleteBtn.addEventListener('click', function() {
                    deleteImage(this.dataset.filename); // Pass the filename to the deleteImage function
                });

                imgContainer.appendChild(img);
                imgContainer.appendChild(deleteBtn);
                gallery.appendChild(imgContainer);
            });
        }
    })
    .catch(error => console.error('Error:', error));
});

function deleteImage(filename) {
    fetch(`/delete/${filename}`, {
        method: 'DELETE'
    })
    .then(response => {
        if (response.ok) {
            // Remove the deleted image from the DOM
            const imageContainer = document.querySelector(`[src="/uploads/${filename}"]`).parentNode;
            imageContainer.remove();
        } else {
            console.error('Failed to delete image');
        }
    })
    .catch(error => console.error('Error:', error));
}
