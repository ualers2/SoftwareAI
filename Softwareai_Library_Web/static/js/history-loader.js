document.addEventListener('DOMContentLoaded', () => {
  const btnHistory = document.querySelector('.tab-button[data-tab="history"]');
  const paneHistory = document.getElementById('history');
  const loaderEl    = document.getElementById('history-loader');
  const params      = new URLSearchParams(window.location.search);
  const agentId     = params.get('agent_id') || params.get('id');
  let loaded = false;

  const renderUseCases = (useCases) => {
    let arr;
    if (Array.isArray(useCases)) arr = useCases;
    else if (useCases && typeof useCases === 'object') arr = Object.values(useCases);
    else if (typeof useCases === 'string') arr = [useCases];
    else arr = [];
    return arr.map(u => `<li>${u}</li>`).join('');
  };

  const renderTools = (tools) => {
    let arr;
    if (Array.isArray(tools)) arr = tools;
    else if (tools && typeof tools === 'object') arr = Object.values(tools);
    else if (typeof tools === 'string') arr = [tools];
    else arr = [];
    return arr
      .map(t => `<span class="inline-block bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded-full mr-2 mb-1">${t}</span>`)
      .join('');
  };

  btnHistory.addEventListener('click', async () => {
    if (loaded) return;
    loaded = true;

    // Cabeçalho + loader
    paneHistory.innerHTML = `<h2 class="text-2xl font-bold mb-6">Version History</h2>`;
    paneHistory.appendChild(loaderEl);

    try {
      const res = await fetch(`/api/agents/history?agent_id=${agentId}`);
      if (!res.ok) throw new Error(`${res.status} ${res.statusText}`);
      const versions = await res.json();
      versions.sort((a, b) => b.timestamp - a.timestamp);

      // remove o loader
      loaderEl.remove();

      // cria container da timeline
      const tl = document.createElement('div');
      tl.className = 'relative';

      // linha central
      const line = document.createElement('div');
      line.className = 'absolute left-1/2 top-0 bottom-0 w-1 bg-gray-200 transform -translate-x-1/2';
      tl.appendChild(line);

      versions.forEach((v, idx) => {
        const isLeft = idx % 2 === 0;
        const wrapper = document.createElement('div');
        wrapper.className = `mb-12 w-full flex ${isLeft ? 'justify-start' : 'justify-end'} items-center`;
        wrapper.innerHTML = `
          <div class="relative w-1/2 ${isLeft ? 'pr-8 text-right' : 'pl-8 text-left'}">
            <!-- dot with icon, overlapping central line -->
            <div class="absolute ${isLeft ? 'right-[-1.75rem]' : 'left-[-1.75rem]'} top-2 w-12 h-12 bg-blue-600 rounded-full flex items-center justify-center border-4 border-white">
              <i class="${v.icon} w-6 h-6 text-white"></i>
            </div>
            <div class="bg-white p-6 rounded-2xl shadow-md">
              <div class="flex justify-between items-center mb-2">
                <h3 class="text-lg font-semibold">Version ${v.version}</h3>
                <time datetime="${new Date(v.timestamp*1000).toISOString()}" class="text-sm text-gray-500">
                  ${new Intl.DateTimeFormat('en-US', {
                    month:'short', day:'numeric', year:'numeric', hour:'2-digit', minute:'2-digit'
                  }).format(new Date(v.timestamp*1000))}
                </time>
              </div>
              <p class="text-gray-700 mb-3">${v.shortDescription}</p>
              <button class="text-blue-600 hover:underline text-sm" onclick="toggleDetails(this)">
                View details
              </button>
              <div class="mt-4 hidden details text-left">
                <p class="mb-2"><strong>Name:</strong> ${v.name}</p>
                <p class="mb-2"><strong>Model:</strong> ${v.model}</p>
                <p class="mb-2"><strong>Tools:</strong><br/>${renderTools(v.tools)}</p>
                <p class="mb-2"><strong>Full Description:</strong> ${v.fullDescription}</p>
                <p class="mb-2"><strong>Instructions:</strong> ${v.instruction}</p>
                <p class="mb-2"><strong>Use Cases:</strong></p>
                <ul class="list-disc pl-5 space-y-1">${renderUseCases(v.UseCases)}</ul>
              </div>
            </div>
          </div>
        `;
        tl.appendChild(wrapper);
      });

      paneHistory.appendChild(tl);

    } catch (err) {
      // garante remoção do loader em caso de erro também
      loaderEl.remove();
      paneHistory.innerHTML += `
        <p class="text-red-500 px-6 py-4">
          Error loading history: ${err.message}
        </p>`;
    }
  });
});

window.toggleDetails = (btn) => {
  const details = btn.parentElement.querySelector('.details');
  details.classList.toggle('hidden');
  btn.textContent = details.classList.contains('hidden')
    ? 'View details' : 'Hide details';
};
