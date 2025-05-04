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
  
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Scraping failed');
      }
  
      const data = await response.json();
      displayAnyData(data);
    } catch (error) {
      resultDiv.innerHTML = `<div class="error">Error: ${error.message}</div>`;
    }
  });
  
  function displayAnyData(data) {
    const resultDiv = document.getElementById('result');
    
    // Handle error responses
    if (data.error) {
      resultDiv.innerHTML = `<div class="error">${data.error}</div>`;
      return;
    }
  
    // Handle empty responses
    if (!data || (typeof data === 'object' && Object.keys(data).length === 0)) {
      resultDiv.innerHTML = '<div class="notice">No data found</div>';
      return;
    }
  
    // Handle string responses
    if (typeof data === 'string') {
      resultDiv.innerHTML = `<div class="text-data">${data}</div>`;
      return;
    }
  
    // Handle array responses
    if (Array.isArray(data)) {
      if (data.length === 0) {
        resultDiv.innerHTML = '<div class="notice">Empty result set</div>';
        return;
      }
      
      // Create a table for array data
      let html = '<table><tr>';
      
      // Generate headers from first object's keys (if array of objects)
      if (typeof data[0] === 'object' && data[0] !== null) {
        Object.keys(data[0]).forEach(key => {
          html += `<th>${key}</th>`;
        });
        html += '</tr>';
        
        // Add rows
        data.forEach(item => {
          html += '<tr>';
          Object.values(item).forEach(value => {
            html += `<td>${formatValue(value)}</td>`;
          });
          html += '</tr>';
        });
      } else {
        // Simple array of values
        html += '<th>Value</th></tr>';
        data.forEach(item => {
          html += `<tr><td>${formatValue(item)}</td></tr>`;
        });
      }
      
      html += '</table>';
      resultDiv.innerHTML = html;
      return;
    }
  
    // Handle object responses
    if (typeof data === 'object') {
      let html = '<div class="object-container">';
      for (const [key, value] of Object.entries(data)) {
        html += `<div class="object-item">
                  <span class="object-key">${key}:</span>
                  <span class="object-value">${formatValue(value)}</span>
                </div>`;
      }
      html += '</div>';
      resultDiv.innerHTML = html;
      return;
    }
  
    // Fallback - just display the raw data
    resultDiv.innerHTML = `<pre>${JSON.stringify(data, null, 2)}</pre>`;
  }
  
  function formatValue(value) {
    if (value === null) return 'null';
    if (value === undefined) return 'undefined';
    if (typeof value === 'object') return JSON.stringify(value);
    return value;
  }