document.getElementById('url-form').addEventListener('submit', function (e) {
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
        <button class="delete"><a href="/delete/${shortUrl}/" style="color: white; text-decoration: none;">Delete</a></button>
    `;

    // Attach an event listener to the update button
    urlDiv.querySelector('.update').addEventListener('click', function () {
        openUpdateModal(shortUrl, longUrl, expirationDate, password, maxUsage);
    });

    shortenedUrlsDiv.appendChild(urlDiv);
}

function openUpdateModal(shortUrl, longUrl, expirationDate, password, maxUsage) {
    // Fetch the updated data from the API (you might need to adjust the endpoint)
    fetch(`/get_url_details/${shortUrl}/`) // Replace with your actual endpoint
        .then(response => response.json())
        .then(data => {
            if (data.data) {
                document.getElementById('shortUrl').value = data.data.shortened_url;
                document.getElementById('update-long-url').value = data.data.long_url;
                document.getElementById('update-expire-date').value = data.data.expiration_time; // Assuming your database stores expiration date as expiration_time
                document.getElementById('update-url-password').value = data.data.password;
                document.getElementById('update-max-usage').value = data.data.max_usage;
                document.getElementById('update-modal').style.display = "block";

                // Update UI after successful fetch
                // Find the existing shortened URL element 
                const existingUrlDiv = document.querySelector('.shortened-url span:first-child b').textContent;
                // Find the parent div
                const parentDiv = existingUrlDiv.parentElement.parentElement;
                // Delete the existing element
                parentDiv.remove();
                // Recreate the element with updated data
                createShortUrlDisplay(
                    data.data.shortened_url,
                    data.data.long_url,
                    data.data.expiration_time,
                    data.data.password,
                    data.data.max_usage
                );
            } else if (data.error) {
                console.error('Error:', data.error);
                // Display error message to the user
            }
        })
        .catch(error => console.error('Error:', error));
}


// Close modal on clicking close button
document.querySelector('.close').addEventListener('click', function () {
    document.getElementById('update-modal').style.display = "none";
});

// Handle update form submission
document.getElementById('update-form').addEventListener('submit', function (e) {
    e.preventDefault();

    const shortUrl = document.getElementById('shortUrl').value;
    const long_url = document.getElementById('update-long-url').value;
    const expiration_time = document.getElementById('update-expire-date').value;
    const password = document.getElementById('update-url-password').value;
    const max_usage = document.getElementById('update-max-usage').value; // Handle potential empty input

    // Send updated data to your API endpoint
    fetch(`/update/${shortUrl}/`, {
        method: 'PUT', // or PATCH depending on your API
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            long_url,
            expiration_time,
            password,
            max_usage // Send as string, handle in the backend
        })
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                console.log('Updated successfully:', data);
                // Close modal and potentially update the UI
                // document.getElementById('update-modal').style.display = "none";
                location.reload();
            } else if (data.error) {
                console.error('Error:', data.error);
                // Display error message to the user
            }
        })
        .catch(error => console.error('Error:', error));
});


// Function to handle password prompt
function promptPassword(shortUrl) {
    document.getElementById('password-modal').style.display = "block"; 
    //  Attach the shortUrl to the submit button so it's available in the submitPassword function
    document.querySelector('#password-modal button[onclick="submitPassword()"]').onclick = function() { submitPassword(shortUrl); };
}

// Function to submit the password
function submitPassword(shortUrl) {
    const password = document.getElementById('password-input').value;
    console.log(password)
    console.log(shortUrl)
    fetch(`/validate-password/${shortUrl}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            password: password
        })
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert("You updated your url successfully! you can check the Database")
                window.location.href = data.redirect_url; 
            } else {
                // Handle incorrect password
                alert('Incorrect password!');
            }
        })
        .catch(error => console.error('Error:', error));
    closeModal();
}

// Function to close the modal
function closeModal() {
    document.getElementById('password-modal').style.display = "none";
}

// Function to handle approval requests
function requestApproval(shortUrl) {
    fetch(`/approve/${shortUrl}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Display success message (or redirect to the original URL)
                alert('URL approved!');
            } else if (data.error) {
                alert(data.error);
            }
        })
        .catch(error => console.error('Error:', error));
}

// Function to fetch and display requests
function fetchRequests() {
    fetch('/pendingApproval_requests/') // Replace with your API endpoint
        .then(response => response.json())
        .then(requests => {
            const requestsSection = document.getElementById('requests-section');
            requestsSection.innerHTML = ''; // Clear existing requests
            
            requests.forEach(request => {
                const requestData = request.fields; // Access the fields
                const requestElement = document.createElement('div');
                requestElement.innerHTML = `
                    <p>User: ${requestData.user}</p>
                    <p>Short URL: ${requestData.url}</p> <!-- Adjust as per your actual data structure -->
                    <button class="approve-button" data-request-id="${request.pk}">Approve</button>
                    <button class="reject-button" data-request-id="${request.pk}">Reject</button>
                `;

                // Attach event listeners to buttons
                requestElement.querySelector('.approve-button').addEventListener('click', handleApprove);
                requestElement.querySelector('.reject-button').addEventListener('click', handleReject);

                requestsSection.appendChild(requestElement);
            });
        })
        .catch(error => console.error('Error fetching requests:', error)); // Handle fetch errors
}


// Function to handle approval
function handleApprove(event) {
    const requestId = event.target.dataset.requestId;
    fetch(`/approve/${requestId}/`, { // Update URL to your API endpoint
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if (response.ok) {
            // Update UI based on response (remove request, etc.)
            event.target.parentElement.remove(); // Remove the request from the list
            // You can add other updates as needed
        } else {
            // Handle error if approval fails
            console.error('Error approving request:', response.status);
        }
    })
    .catch(error => console.error('Error:', error));
}

// Function to handle rejection
function handleReject(event) {
    const requestId = event.target.dataset.requestId;
    fetch(`/reject/${requestId}/`, { // Update URL to your API endpoint
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if (response.ok) {
            // Update UI based on response (remove request, etc.)
            event.target.parentElement.remove(); // Remove the request from the list
            // You can add other updates as needed
        } else {
            // Handle error if rejection fails
            console.error('Error rejecting request:', response.status);
        }
    })
    .catch(error => console.error('Error:', error));
}

// Call fetchRequests initially to load requests
fetchRequests();

