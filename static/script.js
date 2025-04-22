function fetchWeather() {
    const city = document.getElementById('city').value;
    fetch(`/getweather?city=${city}`)
        .then(response => response.json())
        .then(data => {
            const resultDiv = document.getElementById('weatherResult');
            if (data.error) {
                resultDiv.innerHTML = `<p>Error: ${data.error}</p>`;
            } else {
                resultDiv.innerHTML = `<p>City: ${data.city}</p><p>Weather: ${data.weather}</p><p>Temperature: ${data.temperature}</p>`;
            }
        })
        .catch(error => console.error('Error:', error));
}
