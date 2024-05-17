


document.addEventListener('DOMContentLoaded', function() {
    let deleteForm = document.getElementById('delete-form');

    deleteForm.addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent form submission
        let confirmation = confirm("Are you sure you want to delete this book?");
        if (confirmation) {
            // If confirmed, submit the form programmatically
            deleteForm.submit();
        } else {
            console.log("Deletion canceled");
        }
    });
});