document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('scrape-form');
    const resultDiv = document.getElementById('result');
    let downloadButton = document.querySelector('a[href="/download"]');

    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // Show loading state
        resultDiv.innerHTML = '<div class="loading"></div>';
        downloadButton.style.display = 'none';

        try {
            const url = document.getElementById('url').value;
            const response = await fetch('/scrape', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ url: url })
            });

            const data = await response.json();

            if (response.ok) {
                // Display results
                let html = '<div class="results">';
                if (data.data && Array.isArray(data.data)) {
                    data.data.forEach(item => {
                        html += '<div class="quote-item">';
                        if (item.text && item.author) {
                            html += `<p class="quote-text">${item.text}</p>`;
                            html += `<p class="quote-author">- ${item.author}</p>`;
                        } else if (item.content) {
                            html += `<p class="quote-text">${item.content}</p>`;
                        }
                        html += '</div>';
                    });
                }
                html += '</div>';
                resultDiv.innerHTML = html;

                // Show download button and update its state
                downloadButton.style.display = 'inline-block';
                // Force browser to download new file by adding timestamp
                downloadButton.href = `/download?t=${Date.now()}`;
            } else {
                resultDiv.innerHTML = `<div class="error">Error: ${data.message}</div>`;
                downloadButton.style.display = 'none';
            }
        } catch (error) {
            resultDiv.innerHTML = `<div class="error">Error: ${error.message}</div>`;
            downloadButton.style.display = 'none';
        }
    });
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