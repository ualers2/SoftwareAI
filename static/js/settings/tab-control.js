document.querySelectorAll('.tab-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    const tab = btn.getAttribute('data-tab');

    // Resetar botões
    document.querySelectorAll('.tab-btn').forEach(b => {
      b.classList.remove('border-b-2', 'border-blue-600', 'text-white');
      b.classList.add('text-gray-400');
    });

    // Ativar botão clicado
    btn.classList.add('border-b-2', 'border-blue-600', 'text-white');
    btn.classList.remove('text-gray-400');

    // Alternar conteúdo
    document.querySelectorAll('.tab-content').forEach(content => {
      content.classList.add('hidden');
    });
    document.querySelector(`[data-content="${tab}"]`).classList.remove('hidden');
  });
});
