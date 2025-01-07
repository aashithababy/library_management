function toggleSidebar() {
    const sidebar = document.querySelector('.sidebar');
    const isSidebarVisible = sidebar.style.left === '0px';
    sidebar.style.left = isSidebarVisible ? '-200px' : '0px';
}

function logout() {
    alert('Logged out');
    window.location.href = "accounts/login.html";
}