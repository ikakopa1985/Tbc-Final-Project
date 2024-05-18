document.addEventListener("DOMContentLoaded", function () {
    const token = localStorage.getItem('token');

    if (!token) {
        console.error('Token not found in local storage');
        return;
    }

    function apiRequest(url, method, data = null, tokenRequired = true) {
        const headers = { 'Content-Type': 'application/json' };
        if (tokenRequired && token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        return fetch(url, {
            method: method,
            headers: headers,
            body: data ? JSON.stringify(data) : null
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`Network response was not ok: ${response.statusText}`);
            }
            return response.json();
        })
        .catch(error => {
            console.error('There was a problem with your fetch operation:', error);
            throw error;
        });
    }

    // Login form
    document.getElementById("loginForm").addEventListener("submit", function (event) {
        event.preventDefault();
        const username = document.getElementById("username").value;
        const password = document.getElementById("password").value;

        apiRequest('/api/token/', 'POST', { username, password }, false)
            .then(data => {
                localStorage.setItem('token', data.access);
                document.getElementById('token').innerHTML = `Token: ${data.access}`;
                return apiRequest('/api/user-profile/', 'GET');
            })
            .then(profileData => {
                console.log('Authenticated!');
                console.log('User Profile Data:', profileData);
            });
    });

    // Get book by ID
    document.getElementById("sendRequestBtnBookItem").addEventListener("click", function () {
        const bookId = document.getElementById("bookId").value;
        apiRequest(`/books/${bookId}`, 'GET')
            .then(data => {
                document.getElementById('responseApi').innerHTML = JSON.stringify(data);
            });
    });

    // Reserve a book
    document.getElementById('addReserveForm').addEventListener('submit', function(event) {
        event.preventDefault();
        const reserveData = {
            reserve_date: document.getElementById('reserveDate').value,
            book: document.getElementById('bookIdReserve').value,
        };

        apiRequest('/reserves/', 'POST', reserveData)
            .then(data => {
                document.getElementById('responseApi').innerHTML = JSON.stringify(data);
            });
    });

    // Search books
    document.getElementById("searchBut").addEventListener("click", function () {
        const searchKeyword = document.getElementById("searchKeyword").value;
        apiRequest(`/books/?search=${searchKeyword}`, 'GET')
            .then(data => {
                document.getElementById('responseApi').innerHTML = JSON.stringify(data);
            });
    });

    // Filter books by category
    document.getElementById("categoryBut").addEventListener("click", function () {
        const categoryKeyword = document.getElementById("categoryKeyword").value;
        apiRequest(`/books/?category__name=${categoryKeyword}`, 'GET')
            .then(data => {
                document.getElementById('responseApi').innerHTML = JSON.stringify(data);
            });
    });

    // Filter books by author
    document.getElementById("authorBut").addEventListener("click", function () {
        const authorKeyword = document.getElementById("authorKeyword").value;
        apiRequest(`/books/?author__name=${authorKeyword}`, 'GET')
            .then(data => {
                document.getElementById('responseApi').innerHTML = JSON.stringify(data);
            });
    });

    // Pagination
    document.getElementById("paginBut").addEventListener("click", function () {
        const page = document.getElementById("paginKeyword").value;
        apiRequest(`/books/?page=${page}`, 'GET')
            .then(data => {
                document.getElementById('responseApi').innerHTML = JSON.stringify(data);
            });
    });
});
