document.addEventListener('DOMContentLoaded', function () {
    console.log("JavaScript is ready to enhance interactivity.");

    const searchInput = document.getElementById('searchInput');
    const resultsContainer = document.getElementById('results');

    if (searchInput && resultsContainer) {
        searchInput.addEventListener('input', async function () {
            const query = searchInput.value.toLowerCase().trim();
            resultsContainer.innerHTML = ''; // Clear previous results

            if (query.length > 0) {
                try {
                    const response = await fetch(`/api/search-books/?q=${encodeURIComponent(query)}`);
                    const books = await response.json();

                    if (books.length > 0) {
                        books.forEach(book => {
                            const item = document.createElement('div');
                            item.className = 'result-item';

                            const img = document.createElement('img');
                            img.src = book.cover_image || '/static/images/default-cover.jpg';
                            img.alt = book.title;
                            img.className = 'result-cover';

                            const title = document.createElement('span');
                            title.textContent = book.title;
                            title.className = 'result-title';

                            item.appendChild(img);
                            item.appendChild(title);
                            resultsContainer.appendChild(item);
                        });
                    } else {
                        resultsContainer.innerHTML = '<div class="no-results">No matches found</div>';
                    }
                } catch (error) {
                    console.error("Error fetching books:", error);
                    resultsContainer.innerHTML = '<div class="no-results">Error loading results</div>';
                }
            }
        });
    }
});

// Function to fetch books and update the book section
function fetchBooks(category) {
    const url = `/api/get_books/${category}/`;  // API URL to fetch books for a category
    
    fetch(url)
        .then(response => response.json())
        .then(data => {
            const books = data.books;
            const categorySection = document.querySelector(`#${category}-section`);
            categorySection.innerHTML = '';  // Clear existing books

            if (books.length === 0) {
                categorySection.innerHTML = '<p>No books available in this category.</p>';
            } else {
                books.forEach(book => {
                    const bookFrame = document.createElement('div');
                    bookFrame.classList.add('book-frame');

                    // Add book content dynamically
                    const bookImage = document.createElement('img');
                    bookImage.src = book.cover_image;
                    bookImage.alt = book.title;

                    const bookTitle = document.createElement('div');
                    bookTitle.classList.add('book-title');
                    bookTitle.innerText = book.title;

                    const bookAuthor = document.createElement('div');
                    bookAuthor.classList.add('book-author');
                    bookAuthor.innerText = `By: ${book.author}`;

                    const bookDescription = document.createElement('div');
                    bookDescription.classList.add('book-description');
                    bookDescription.innerText = book.description || 'No description available.';

                    const bookPrice = document.createElement('div');
                    bookPrice.classList.add('book-price');
                    bookPrice.innerText = `Price: $${book.price}`;

                    const buyButton = document.createElement('a');
                    buyButton.classList.add('buy-button');
                    buyButton.href = book.detail_page;
                    buyButton.innerText = 'View';

                    // Append to book frame
                    bookFrame.appendChild(bookImage);
                    bookFrame.appendChild(bookTitle);
                    bookFrame.appendChild(bookAuthor);
                    bookFrame.appendChild(bookDescription);
                    bookFrame.appendChild(bookPrice);
                    bookFrame.appendChild(buyButton);

                    // Append book frame to category section
                    categorySection.appendChild(bookFrame);
                });
            }
        })
        .catch(error => {
            console.error('Error fetching books:', error);
        });
}

// Fetch books initially for each category
document.addEventListener('DOMContentLoaded', function () {
    fetchBooks('bestsellers');
    fetchBooks('early_releases');
    fetchBooks('trending');
    fetchBooks('fiction');
    fetchBooks('nonfiction');
});
