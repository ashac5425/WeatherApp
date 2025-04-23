function fetchWeather() {
    const city = document.getElementById('city').value;
    fetch(`/getweather?city=${city}`)
        .then(response => response.json())
        .then(data => {
            const resultDiv = document.getElementById('weatherResult');
            if (data.error) {
                resultDiv.innerHTML = `<p>Error: ${data.error}</p>`;
            } else {
                resultDiv.innerHTML = `
                    <p><strong>City:</strong> ${data.city}</p>
                    <p><strong>Temperature:</strong> ${data.temperature}</p>
                    <p><strong>Humidity:</strong> ${data.humidity}</p>
                    <p><strong>Wind:</strong> ${data.wind}</p>
                `;
            }
        })
        .catch(error => console.error('Error:', error));
}
