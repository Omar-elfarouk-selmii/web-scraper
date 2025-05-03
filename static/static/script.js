document.getElementById('scrape-form').addEventListener('submit', async function(e) {
  e.preventDefault();
  const url = document.getElementById('url').value;
  const resultDiv = document.getElementById('result');
  resultDiv.innerHTML = 'Scraping in progress...';

  try {
      const response = await fetch('http://localhost:5000/scrape', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ url: url })
      });

      if (!response.ok) throw new Error('Scraping failed.');

      const data = await response.json();
      displayResults(data);
  } catch (error) {
      resultDiv.innerHTML = `Error: ${error.message}`;
  }
});

document.getElementById('author-form').addEventListener('submit', async function(e) {
  e.preventDefault();
  const author = document.getElementById('author').value;
  const resultDiv = document.getElementById('result');
  resultDiv.innerHTML = 'Fetching quotes...';

  try {
      const response = await fetch(`http://localhost:5000/quotes/${encodeURIComponent(author)}`, {
          method: 'GET'
      });

      if (!response.ok) throw new Error('No quotes found.');

      const data = await response.json();
      displayResults(data);
  } catch (error) {
      resultDiv.innerHTML = `Error: ${error.message}`;
  }
});

function displayResults(data) {
  const resultDiv = document.getElementById('result');
  if (!data || data.message) {
      resultDiv.innerHTML = data.message || 'No data available.';
      return;
  }

  let html = '<table><tr><th>Quote</th><th>Author</th></tr>';
  data.forEach(item => {
      html += `<tr><td>${item.text}</td><td>${item.author}</td></tr>`;
  });
  html += '</table>';
  resultDiv.innerHTML = html;
}