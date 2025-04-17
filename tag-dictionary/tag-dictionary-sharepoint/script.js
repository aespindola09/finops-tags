async function loadTags() {
  const response = await fetch('tags.json');
  const tags = await response.json();
  renderTable(tags);

  document.getElementById('filter-nube').addEventListener('change', () => renderTable(tags));
  document.getElementById('filter-required').addEventListener('change', () => renderTable(tags));
  document.getElementById('search').addEventListener('input', () => renderTable(tags));
}

function renderTable(tags) {
  const nubeFilter = document.getElementById('filter-nube').value;
  const requiredFilter = document.getElementById('filter-required').value;
  const search = document.getElementById('search').value.toLowerCase();

  const tbody = document.querySelector('#tag-table tbody');
  tbody.innerHTML = '';

  const filtered = tags.filter(tag => {
    const matchesNube = nubeFilter === 'todas' || tag.applies_to.includes(nubeFilter);
    const matchesRequired = requiredFilter === 'todos' || String(tag.required) === requiredFilter;
    const matchesSearch = tag.key.toLowerCase().includes(search);
    return matchesNube && matchesRequired && matchesSearch;
  });

  filtered.forEach(tag => {
    const row = document.createElement('tr');
    row.innerHTML = `
      <td>${tag.key}</td>
      <td>${tag.description}</td>
      <td>${tag.required ? 'Sí' : 'No'}</td>
      <td>${tag.allowed_values.join(', ') || '-'}</td>
      <td>${tag.applies_to.join(', ')}</td>
    `;
    tbody.appendChild(row);
  });
}

loadTags();