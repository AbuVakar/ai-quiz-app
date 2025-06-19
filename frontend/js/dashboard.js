document.addEventListener('DOMContentLoaded', function() {
    const confirmDeleteButton = document.getElementById('confirmDelete');
    const deletePasswordInput = document.getElementById('deletePassword');
    const deleteAccountForm = document.getElementById('deleteAccountForm');

    if (confirmDeleteButton) {
        confirmDeleteButton.addEventListener('click', async function() {
            const password = deletePasswordInput.value;
            
            try {
                const response = await fetch('/delete-account', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ password: password })
                });

                const data = await response.json();

                if (response.ok) {
                    // Account deleted successfully
                    alert('Your account has been deleted successfully');
                    window.location.href = '/';
                } else {
                    // Handle error
                    alert(data.error || 'Failed to delete account');
                }
            } catch (error) {
                console.error('Error:', error);
                alert('An error occurred while trying to delete your account');
            }
        });
    }
});
