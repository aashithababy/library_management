// scripts.js
document.addEventListener('DOMContentLoaded', function() {
    console.log("JavaScript is ready to enhance interactivity.");
    // Add custom interactivity here, e.g., dynamic content loading, filters
});


document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('searchInput');
    const resultsContainer = document.getElementById('results');

    searchInput.addEventListener('input', function() {
        const query = searchInput.value.toLowerCase();
        resultsContainer.innerHTML = ''; // Clear previous results

        if (query.length > 0) {
            // Example static search results
            const books = [
                'Quarter to Midnight',
                'The Blue Hour',
                'A Vile Season',
                'Curdle Creek',
                'For She is Wrath'
            ];

            const filteredBooks = books.filter(book => book.toLowerCase().includes(query));

            if (filteredBooks.length > 0) {
                filteredBooks.forEach(book => {
                    const item = document.createElement('div');
                    item.textContent = book;
                    item.className = 'result-item';
                    resultsContainer.appendChild(item);
                });
            } else {
                resultsContainer.innerHTML = '<div class="no-results">No matches found</div>';
            }
        }
    });
});
