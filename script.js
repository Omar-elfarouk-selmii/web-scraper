document.getElementById('scrape-form').addEventListener('submit', async function(e) {
  e.preventDefault();
  const url = document.getElementById('url').value;
  const resultDiv = document.getElementById('result');
  resultDiv.textContent = "Scraping in progress...";

  try {
    // Call your backend endpoint here
    const response = await fetch('http://localhost:5000/scrape', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url: url })
    });

    if (!response.ok) throw new Error('Scraping failed.');

    const data = await response.json();
    resultDiv.textContent = data.result || JSON.stringify(data, null, 2);
  } catch (error) {
    resultDiv.textContent = 'Error: ' + error.message;
  }
});
