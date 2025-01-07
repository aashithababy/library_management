document.addEventListener('DOMContentLoaded', function () {
    const authorInput = document.getElementById('id_authors_name');  // Target the input field by its ID
    if (!authorInput) return;

    const searchURL = authorInput.dataset.searchUrl;

    authorInput.addEventListener('input', function () {
        const query = authorInput.value;

        if (query.length > 2) {  // Start searching after 2 characters
            fetch(`${searchURL}?name=${encodeURIComponent(query)}`)
                .then(response => response.json())
                .then(data => {
                    // Display suggestions
                    const suggestions = data.suggestions || [];
                    let suggestionHTML = suggestions.map(author => `<li>${author}</li>`).join('');
                    if (!suggestions.length) {
                        suggestionHTML = '<li>No authors found</li>';
                    }

                    let dropdown = document.getElementById('author-suggestions');
                    if (!dropdown) {
                        dropdown = document.createElement('ul');
                        dropdown.id = 'author-suggestions';
                        dropdown.style.position = 'absolute';
                        dropdown.style.backgroundColor = 'white';
                        dropdown.style.border = '1px solid #ccc';
                        authorInput.parentNode.appendChild(dropdown);
                    }
                    dropdown.innerHTML = suggestionHTML;

                    // Add click events for suggestions
                    dropdown.querySelectorAll('li').forEach(item => {
                        item.addEventListener('click', () => {
                            authorInput.value = item.textContent;
                            dropdown.innerHTML = '';  // Clear suggestions
                        });
                    });
                })
                .catch(error => console.error('Error fetching author suggestions:', error));
        }
    });
});
