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