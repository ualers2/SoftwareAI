const toggleButton = document.getElementById('toggle-sidebar');
const sidebar = document.getElementById('chat-sidebar');

const backdrop = document.getElementById('sidebar-backdrop');

function toggleSidebar() {
  const isOpen = !sidebar.classList.contains('-translate-x-full');

  if (isOpen) {
    // Fecha
    sidebar.classList.add('-translate-x-full');
    backdrop.classList.add('hidden');
  } else {
    // Abre
    sidebar.classList.remove('-translate-x-full');
    backdrop.classList.remove('hidden');
  }
}

toggleButton.addEventListener('click', toggleSidebar);

backdrop.addEventListener('click', () => {
  sidebar.classList.add('-translate-x-full');
  backdrop.classList.add('hidden');
});
