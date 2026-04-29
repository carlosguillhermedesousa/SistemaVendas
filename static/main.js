document.addEventListener('DOMContentLoaded', function () {
  document.body.classList.add('fade-in');

  const filters = document.querySelectorAll('[data-search-target]');

  filters.forEach(input => {
    const targetSelector = input.dataset.searchTarget;
    const target = document.querySelector(targetSelector);
    if (!target) return;

    input.addEventListener('input', () => {
      const searchValue = input.value.toLowerCase().trim();

      if (target.tagName === 'TABLE') {
        const rows = target.querySelectorAll('tbody tr');
        rows.forEach(row => {
          const text = row.textContent.toLowerCase();
          row.style.display = text.includes(searchValue) ? '' : 'none';
        });
      }

      if (target.tagName === 'SELECT') {
        const options = target.querySelectorAll('option');
        options.forEach(option => {
          const text = option.textContent.toLowerCase();
          const showOption = !searchValue || text.includes(searchValue);
          option.style.display = showOption ? '' : 'none';
        });
      }
    });
  });

  const setupTablePagination = (tableId, searchId, itemsId, paginationId, noResultsMessage) => {
    const table = document.getElementById(tableId);
    const searchInput = document.getElementById(searchId);
    const itemsPerPage = document.getElementById(itemsId);
    const paginationControls = document.getElementById(paginationId);
    if (!table || !searchInput || !itemsPerPage || !paginationControls) return;

    const rows = Array.from(table.querySelectorAll('tbody tr[data-row]'));
    let currentPage = 1;

    const renderPagination = (visibleCount, pageSize) => {
      const totalPages = Math.max(1, Math.ceil(visibleCount / pageSize));
      paginationControls.innerHTML = '';

      const createPageItem = (page, label, active = false, disabled = false) => {
        const li = document.createElement('li');
        li.className = `page-item ${active ? 'active' : ''} ${disabled ? 'disabled' : ''}`;
        li.innerHTML = `<button type="button" class="page-link">${label}</button>`;
        if (!disabled) {
          li.querySelector('button').addEventListener('click', () => {
            currentPage = page;
            updateTable();
          });
        }
        paginationControls.appendChild(li);
      };

      createPageItem(currentPage - 1, 'Anterior', false, currentPage === 1);
      for (let i = 1; i <= totalPages; i++) {
        createPageItem(i, i, currentPage === i);
      }
      createPageItem(currentPage + 1, 'Próximo', false, currentPage === totalPages);
    };

    const updateTable = () => {
      const query = searchInput.value.toLowerCase().trim();
      const visibleRows = rows.filter(row => row.textContent.toLowerCase().includes(query));
      const pageSize = Number(itemsPerPage.value) || 15;
      const totalPages = Math.max(1, Math.ceil(visibleRows.length / pageSize));
      if (currentPage > totalPages) currentPage = totalPages;

      table.querySelectorAll('tbody tr').forEach(row => row.style.display = 'none');
      const existingEmpty = table.querySelector('.no-results');
      if (existingEmpty) existingEmpty.remove();

      if (!visibleRows.length) {
        const tr = document.createElement('tr');
        tr.className = 'no-results';
        tr.innerHTML = `<td colspan="${table.querySelectorAll('thead th').length}" class="text-center text-muted">${noResultsMessage}</td>`;
        table.querySelector('tbody').appendChild(tr);
      } else {
        const start = (currentPage - 1) * pageSize;
        const end = start + pageSize;
        visibleRows.slice(start, end).forEach(row => row.style.display = '');
      }

      renderPagination(visibleRows.length, pageSize);
    };

    itemsPerPage.addEventListener('change', () => {
      currentPage = 1;
      updateTable();
    });

    searchInput.addEventListener('input', () => {
      currentPage = 1;
      updateTable();
    });

    updateTable();
  };

  setupTablePagination('customersTable', 'searchClients', 'itemsPerPage', 'paginationControls', 'Nenhum cliente encontrado.');
  setupTablePagination('productsTable', 'searchProducts', 'itemsPerPageProducts', 'paginationControlsProducts', 'Nenhum produto encontrado.');
  setupTablePagination('paymentMethodsTable', 'searchPaymentMethods', 'itemsPerPagePaymentMethods', 'paginationControlsPaymentMethods', 'Nenhuma forma de pagamento encontrada.');
  setupTablePagination('usersTable', 'searchUsers', 'itemsPerPageUsers', 'paginationControlsUsers', 'Nenhum usuário encontrado.');
  setupTablePagination('stockMovementsTable', 'searchStockMovements', 'itemsPerPageStockMovements', 'paginationControlsStockMovements', 'Nenhuma movimentação encontrada.');

  const internalLinks = Array.from(document.querySelectorAll('a[href]')).filter(link => {
    return link.target !== '_blank' && link.href.startsWith(window.location.origin) && !link.href.includes('mailto:') && !link.hash.startsWith('#');
  });

  internalLinks.forEach(link => {
    link.addEventListener('click', event => {
      event.preventDefault();
      document.body.classList.remove('fade-in');
      document.body.classList.add('fade-out');
      setTimeout(() => window.location.href = link.href, 220);
    });
  });

  window.addEventListener('pageshow', event => {
    if (event.persisted) {
      window.location.reload();
    }
  });

  const chartCanvas = document.querySelector('#salesChart');
  if (chartCanvas) {
    const labels = JSON.parse(chartCanvas.dataset.labels);
    const values = JSON.parse(chartCanvas.dataset.values);
    new Chart(chartCanvas, {
      type: 'line',
      data: {
        labels: labels,
        datasets: [{
          label: 'Vendas recentes',
          data: values,
          borderColor: '#38bdf8',
          backgroundColor: 'rgba(56, 189, 248, 0.16)',
          pointBackgroundColor: '#22c55e',
          tension: 0.35,
          borderWidth: 3,
          fill: true,
        }]
      },
      options: {
        responsive: true,
        plugins: {
          legend: { display: false },
          tooltip: { mode: 'index', intersect: false }
        },
        scales: {
          x: { grid: { color: 'rgba(148, 163, 184, 0.12)' }, ticks: { color: '#cbd5e1' } },
          y: { grid: { color: 'rgba(148, 163, 184, 0.12)' }, ticks: { color: '#cbd5e1' } }
        }
      }
    });
  }

  const toasts = document.querySelectorAll('.toast');
  if (toasts.length) {
    toasts.forEach(toastEl => {
      new bootstrap.Toast(toastEl).show();
    });
  }
});
