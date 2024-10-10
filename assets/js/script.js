document.getElementById('url-form').addEventListener('submit', function(e) {
    e.preventDefault();

    const longUrl = document.getElementById('long-url').value;
    const expirationDate = document.getElementById('expire-date').value;
    const password = document.getElementById('url-password').value;
    const maxUsage = document.getElementById('max-usage').value; // Handle the potential empty input

    // Send data to your API endpoint
    fetch('/create/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            long_url: longUrl,
            expiration_date: expirationDate,
            password: password,
            max_usage: maxUsage // Send as string, handle in the backend
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.data) {
            createShortUrlDisplay(data.data.shortened_url, longUrl, expirationDate, password, maxUsage);
            document.getElementById('url-form').reset(); // Reset form
        } else if (data.error) {
            console.error('Error:', data.error);
            // Display error message to the user
        }
    })
    .catch(error => console.error('Error:', error));
});

function createShortUrlDisplay(shortUrl, longUrl, expirationDate, password, maxUsage) {
    const shortenedUrlsDiv = document.getElementById('shortened-urls');
    
    const urlDiv = document.createElement('div');
    urlDiv.classList.add('shortened-url');

    urlDiv.innerHTML = `
        <span><strong>Short URL:</strong> <b>${shortUrl}</b></span>
        <span><strong>Long URL:</strong> <b>${longUrl}</b></span>
        <span><strong>Expires:</strong> <b>${expirationDate || 'N/A'}</b></span>
        <span><strong>Password:</strong> <b>${password ? 'Yes' : 'No'}</b></span>
        <span><strong>Max Uses:</strong> <b>${maxUsage ? maxUsage : 'Unlimited'}</b></span>
        <button class="update">Update</button>
        <button class="delete"><a href="YOUR_DELETE_ENDPOINT_HERE?shortUrl=${shortUrl}" style="color: white; text-decoration: none;">Delete</a></button>
    `;

    // Attach an event listener to the update button
    urlDiv.querySelector('.update').addEventListener('click', function() {
        openUpdateModal(longUrl, expirationDate, password, maxUsage);
    });

    shortenedUrlsDiv.appendChild(urlDiv);
}

function openUpdateModal(longUrl, expirationDate, password, maxUsage) {
    // Set values in update form
    document.getElementById('update-long-url').value = longUrl;
    document.getElementById('update-expire-date').value = expirationDate;
    document.getElementById('update-url-password').value = password;
    document.getElementById('update-max-usage').value = maxUsage;

    // Show modal
    document.getElementById('update-modal').style.display = "block";
}

// Close modal on clicking close button
document.querySelector('.close').addEventListener('click', function() {
    document.getElementById('update-modal').style.display = "none";
});

// Handle update form submission
document.getElementById('update-form').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const updatedLongUrl = document.getElementById('update-long-url').value;
    const updatedExpireDate = document.getElementById('update-expire-date').value;
    const updatedPassword = document.getElementById('update-url-password').value;
    const updatedMaxUsage = document.getElementById('update-max-usage').value; // Handle potential empty input

    // Send updated data to your API endpoint
    fetch(`/update/${updatedLongUrl}/`, {
        method: 'PUT', // or PATCH depending on your API
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            updatedLongUrl,
            updatedExpireDate,
            updatedPassword,
            updatedMaxUsage // Send as string, handle in the backend
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log('Updated successfully:', data);
            // Close modal and potentially update the UI
            document.getElementById('update-modal').style.display = "none";
        } else if (data.error) {
            console.error('Error:', data.error);
            // Display error message to the user
        }
    })
    .catch(error => console.error('Error:', error));
});
