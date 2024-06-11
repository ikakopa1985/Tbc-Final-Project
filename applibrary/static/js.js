document.addEventListener("DOMContentLoaded", function () {
    const token = localStorage.getItem('token');

    if (!token) {
        console.error('Token not found in local storage');
    } else {
        apiRequest('/api/user-profile/', 'GET')
            .then(profileData => {
                console.log('Authenticated!');
                console.log('User Profile Data:', profileData);
                document.getElementById('token').innerHTML =
                    document.getElementById('token').innerHTML +
                    '           welcome   ' +
                    '            \n    ' +
                    'email=' + profileData['email'] +
                    '            \n    ' +
                    'username= ' + profileData['username']
            });
    }

    async function refreshAccessToken() {
        const refreshToken = localStorage.getItem('refresh_token');
        if (!refreshToken) {
            console.error('Refresh token not found in local storage');
            return null;
        }

        try {
            const response = await fetch('/api/token/refresh/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ refresh: refreshToken })
            });

            if (response.ok) {
                const data = await response.json();
                localStorage.setItem('token', data.access);
                return data.access;
            } else {
                console.error('Failed to refresh access token:', response.statusText);
                return null;
            }
        } catch (error) {
            console.error('Error refreshing access token:', error);
            return null;
        }
    }

    async function apiRequest(url, method, data = null, tokenRequired = true) {
        const headers = { 'Content-Type': 'application/json' };
        let token = localStorage.getItem('token');

        if (tokenRequired && token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        try {
            let response = await fetch(url, {
                method: method,
                headers: headers,
                body: data ? JSON.stringify(data) : null
            });

            if (response.status === 401 && tokenRequired) { // If unauthorized, try to refresh the token
                token = await refreshAccessToken();
                if (token) {
                    headers['Authorization'] = `Bearer ${token}`;
                    response = await fetch(url, {
                        method: method,
                        headers: headers,
                        body: data ? JSON.stringify(data) : null
                    });
                } else {
                    throw new Error('Unable to refresh token');
                }
            }

            if (!response.ok) {
                throw new Error(`Network response was not ok: ${response.statusText}`);
            }

            return response.json();
        } catch (error) {
            console.error('There was a problem with your fetch operation:', error);
            throw error;
        }
    }

    // Login form
    document.getElementById("loginForm").addEventListener("submit", function (event) {
        event.preventDefault();
        const username = document.getElementById("username").value;
        const password = document.getElementById("password").value;

        apiRequest('/api/token/', 'POST', { username, password }, false)
            .then(data => {
                localStorage.setItem('token', data.access);
                localStorage.setItem('refresh_token', data.refresh);
                document.getElementById('token').innerHTML = `Token: ${data.access}`;
                return apiRequest('/api/user-profile/', 'GET');
            })
            .then(profileData => {
                console.log('Authenticated!');
                console.log('User Profile Data:', profileData);
                document.getElementById('token').innerHTML =
                    document.getElementById('token').innerHTML +
                    '            \n    ' +
                    'email=' + profileData['email'] +
                    '            \n    ' +
                    'username= ' + profileData['username']
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

    // Create user
    document.getElementById('userIdentForm').addEventListener('submit', async function(event) {
        event.preventDefault();
        const userData = {
            username: document.getElementById('usernameCreate').value,
            password: document.getElementById('passwordCreate').value,
            email: document.getElementById('email').value,
            first_name: document.getElementById('firstname').value,
            last_name: document.getElementById('lastname').value,
        };
        const userIdentData = {
            full_name: document.getElementById('full_name').value,
            personal_number: document.getElementById('personal_number').value,
            birth_date: document.getElementById('birth_date').value,
            user: userData,
        };
        try {
            const response = await fetch('/users/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(userIdentData),
            });
            if (response.ok) {
                const result = await response.json();
                alert('UserIdent created successfully!');
                console.log(result);
            } else {
                const error = await response.json();
                alert('Error creating UserIdent: ' + JSON.stringify(error));
                console.error('Error:', error);
            }
        } catch (error) {
            alert('Network error: ' + error.message);
            console.error('Network error:', error);
        }
    });

    // Get 10 Popular Books
    document.getElementById("get10PopularBooksBut").addEventListener("click", function () {
        apiRequest(`/get10PopularBooks`, 'GET')
            .then(data => {
                document.getElementById('responseApi').innerHTML = JSON.stringify(data);
            });
    });

    // Get All Book Lease 1 Year
    document.getElementById("getAllBookLease1YearBut").addEventListener("click", function () {
        console.log('clicked')
        apiRequest(`/getAllBookLease1Year`, 'GET')
            .then(data => {
                document.getElementById('responseApi').innerHTML = JSON.stringify(data);
            });
    });

    // Get 100 Book Most Overdue
    document.getElementById("get100BookMostOverdueBut").addEventListener("click", function () {
        console.log('clicked')
        apiRequest(`/get100BookMostOverdue`, 'GET')
            .then(data => {
                document.getElementById('responseApi').innerHTML = JSON.stringify(data);
            });
    });

    // Get 100 User Most Overdue
    document.getElementById("get100UserMostOverdueBut").addEventListener("click", function () {
        console.log('clicked')
        apiRequest(`/get100UserMostOverdue`, 'GET')
            .then(data => {
                document.getElementById('responseApi').innerHTML = JSON.stringify(data);
            });
    });

    // Get Sorted Books
    document.getElementById("getSortedBooksBut").addEventListener("click", function () {
        console.log('clicked')
        apiRequest(`/getSortedBooks`, 'GET')
            .then(data => {
                document.getElementById('responseApi').innerHTML = JSON.stringify(data);
            });
    });

    // Add to Wishlist
    document.getElementById('addtowishlistform').addEventListener('submit', function(event) {
        event.preventDefault();
        const wishlistData = {
            book: document.getElementById('bookidinput').value,
        };

        apiRequest('/wishlist/', 'POST', wishlistData)
            .then(data => {
                document.getElementById('responseApi').innerHTML = JSON.stringify(data);
            });
    });
});
