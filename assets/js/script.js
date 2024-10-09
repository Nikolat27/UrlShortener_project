document.getElementById('url-form').addEventListener('submit', function(e) {
    e.preventDefault();

    const long_url = document.getElementById('long-url').value;
    const expiration_date = document.getElementById('expire-date').value;
    const password = document.getElementById('url-password').value;
    const max_usage = document.getElementById('max-usage').value;

    // Send data to your API endpoint
    fetch('http://127.0.0.1:8000/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            long_url,
            expiration_date,
            password,
            max_usage
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data)
        // Assuming the API returns the short URL and other info
        createShortUrlDisplay(data.shortUrl, long_url, expiration_date, password, max_usage);
        document.getElementById('url-form').reset(); // Reset form
    })
    .catch(error => console.error('Error:', error));
});

function createShortUrlDisplay(shortUrl, long_url, expiration_date, password, max_usage) {
    const shortenedUrlsDiv = document.getElementById('shortened-urls');
    
    const urlDiv = document.createElement('div');
    urlDiv.classList.add('shortened-url');

    urlDiv.innerHTML = `
        <span><strong>Short URL:</strong> <b>${shortUrl}</b></span>
        <span><strong>Long URL:</strong> <b>${long_url}</b></span>
        <span><strong>Expires:</strong> <b>${expiration_date || 'N/A'}</b></span>
        <span><strong>Password:</strong> <b>${password ? 'Yes' : 'No'}</b></span>
        <span><strong>Max Uses:</strong> <b>${max_usage || 'Unlimited'}</b></span>
        <button class="update">Update</button>
        <button class="delete"><a href="YOUR_DELETE_ENDPOINT_HERE?shortUrl=${shortUrl}" style="color: white; text-decoration: none;">Delete</a></button>
    `;

    // Attach an event listener to the update button
    urlDiv.querySelector('.update').addEventListener('click', function() {
        openUpdateModal(long_url, expiration_date, password, max_usage);
    });

    shortenedUrlsDiv.appendChild(urlDiv);
}

function openUpdateModal(long_url, expiration_date, password, max_usage) {
    // Set values in update form
    document.getElementById('update-long-url').value = long_url;
    document.getElementById('update-expire-date').value = expiration_date;
    document.getElementById('update-url-password').value = password;
    document.getElementById('update-max-usage').value = max_usage;

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
    const updatedMaxUsage = document.getElementById('update-max-usage').value;

    // Send updated data to your API endpoint
    fetch('YOUR_UPDATE_API_ENDPOINT_HERE', {
        method: 'PUT', // or PATCH depending on your API
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            updatedLongUrl,
            updatedExpireDate,
            updatedPassword,
            updatedMaxUsage
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Updated successfully:', data);
        // Close modal and potentially update the UI
        document.getElementById('update-modal').style.display = "none";
    })
    .catch(error => console.error('Error:', error));
});
