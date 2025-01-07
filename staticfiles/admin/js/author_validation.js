document.addEventListener('DOMContentLoaded', function() {
    const authorInput = document.getElementById('author-name-input');

    if (authorInput) {
        authorInput.addEventListener('input', function() {
            const authorName = authorInput.value;
            if (authorName.length > 2) {
                fetch(`/catalog/search-author/?name=${encodeURIComponent(authorName)}`)
                    .then(response => response.json())
                    .then(data => {
                        if (!data.exists) {
                            if (confirm(`Author "${authorName}" does not exist. Do you want to add this author?`)) {
                                window.location.href = '/catalog/add-author/';
                            }
                        }
                    })
                    .catch(error => console.error('Error:', error));
            }
        });
    }
});
