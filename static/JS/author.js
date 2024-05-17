document.addEventListener('DOMContentLoaded', function() {
    let deleteForms = document.querySelectorAll('.delete-form');

    deleteForms.forEach(function(deleteForm) {
        deleteForm.addEventListener('submit', function(event) {
            event.preventDefault(); // Prevent form submission
            let confirmation = confirm("Are you sure you want to delete this author?");
            if (confirmation) {
                // If confirmed, submit the form programmatically
                deleteForm.submit();
            } else {
                console.log("Deletion canceled");
            }
        });
    });
});
