const toggleBtn = document.getElementById('theme-toggle');
const currentTheme = localStorage.getItem('theme');

if (currentTheme === 'light') {
    document.body.classList.add('light-mode');
    toggleBtn.textContent = 'Dark Mode';
}

toggleBtn.addEventListener('click', () => {
    document.body.classList.toggle('light-mode');
    let theme = 'dark';
    if (document.body.classList.contains('light-mode')) {
        theme = 'light';
        toggleBtn.textContent = 'Dark Mode';
    } else {
        toggleBtn.textContent = 'Light Mode';
    }
    localStorage.setItem('theme', theme);
});

async function shortenUrl() {
    const urlInput = document.getElementById('longUrl').value;
    const customAlias = document.getElementById('customAlias').value;
    const expiryTime = document.getElementById('expiryTime').value;
    
    const resultDiv = document.getElementById('result');
    const errorDiv = document.getElementById('errorMsg');
    resultDiv.innerHTML = "";
    errorDiv.innerText = "";
    if (!urlInput) {
        errorDiv.innerText = "Please enter a URL!";
        return;
    }
    const response = await fetch('/api/shorten', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
            original_url: urlInput,
            custom_alias: customAlias,
            expires_in_hours: expiryTime
        })
    });
    const data = await response.json();
    if (response.ok) {
        resultDiv.innerHTML = `Success! <br><br> <a href="${data.short_url}" target="_blank">${data.short_url}</a>`;
    } else {
        errorDiv.innerText = data.error || "Something went wrong.";
    }
}