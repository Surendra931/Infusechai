// JavaScript function to update item quantity in the cart
function updateQuantity(itemId, change) {  // Function to increase or decrease quantity
  const url = `/update-quantity/${itemId}/`;  // Endpoint to handle quantity update
  const data = {  // Data to send in the POST request
      'change': change
  };

  // Send a POST request to update the quantity
  fetch(url, {
      method: 'POST',  // POST method
      headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': '{{ csrf_token }}'  // CSRF token for security
      },
      body: JSON.stringify(data)  // Convert data to JSON format
  }).then(response => {
      if (response.ok) {
          window.location.reload();  // Reload the page after successful update
      } else {
          console.error('Failed to update quantity');  // Handle error
      }
  });
}
