//QUESTION 1

function fetchUniqueCharacterData() {
    fetch('/distinct_characters')
        .then(response => response.json())
        .then(data => {
            const characterDropdown = document.getElementById('character-dropdown');
            characterDropdown.innerHTML = '';  // Clear previous options

            data.forEach(item => {
                const option = document.createElement('option');
                option.value = item._id;  // Character name
                option.textContent = `${item._id} (${item.Alignment})`;  // Displayed as "Character Name (Alignment)"
                characterDropdown.appendChild(option);
            });
        })
        .catch(error => console.error('Error fetching unique character data:', error));
}

function searchCharacter(event) {
    event.preventDefault();
    const characterName = document.getElementById('character-name').value;

    fetch(`/character_search?character_name=${characterName}`)
        .then(response => response.json())
        .then(data => {
            const resultSection = document.getElementById('result-section');
            const alignmentResult = document.getElementById('alignment-result');

            // Clear previous content
            alignmentResult.innerHTML = '';

            if (data.error) {
                // Display the error message
                alignmentResult.innerHTML = `<p style="color: red;">${data.error}</p>`;
            } else {
                // Display each unique character name with their alignment
                alignmentResult.innerHTML = '<ul>';  // Start unordered list
                const uniqueCharacterData = new Map();
                data.forEach(instance => {
                    const name = instance.Name;
                    const alignment = instance.Alignment;
                    if (!uniqueCharacterData.has(name)) {
                        uniqueCharacterData.set(name, alignment);
                    }
                });
                uniqueCharacterData.forEach((alignment, name) => {
                    alignmentResult.innerHTML += `<li>${name} (${alignment})</li>`;
                });
                alignmentResult.innerHTML += '</ul>';  // End unordered list
            }

            // Always display the result section
            resultSection.style.display = 'block';
        })
        .catch(error => {
            console.error('Error:', error);
            const resultSection = document.getElementById('result-section');
            resultSection.style.display = 'block';
            const alignmentResult = document.getElementById('alignment-result');
            alignmentResult.innerHTML = `<p style="color: red;">An error occurred. Please try again.</p>`;
        });
}


//QUESTION 4
let mpaRatingChart;		
		
function createOrUpdateBarChart(labels, values) {
    const ctx = document.getElementById('mpa-rating-chart').getContext('2d');

    if (mpaRatingChart) {
        mpaRatingChart.data.labels = labels;
        mpaRatingChart.data.datasets[0].data = values;
        mpaRatingChart.update();
    } else {
        mpaRatingChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Gross Income',
                    data: values,
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }
}

document.addEventListener('DOMContentLoaded', function () {
    const mpaChartCanvas = document.getElementById('mpa-rating-chart');

    const getMplChart = async () => {
        try {
            const response = await fetch('/get_mpl_chart');
            const data = await response.json();

            // Create an image element to display the Matplotlib chart
            const img = document.createElement('img');
            img.src = `data:image/png;base64,${data.image_base64}`;
            mpaChartCanvas.appendChild(img);
        } catch (error) {
            console.error('Error fetching Matplotlib chart:', error);
        }
    };

    const searchButton = document.getElementById('search-button-mpa');
    searchButton.addEventListener('click', getMplChart);
});

document.addEventListener('DOMContentLoaded', fetchUniqueCharacterData);

//QUESTION 2

function searchCharacterQ2(event) {
    event.preventDefault();
    const characterName = document.getElementById('character-name').value;

    fetch(`/character_search?character_name=${characterName}`)
        .then(response => response.json())
        .then(data => {
            const resultSection = document.getElementById('result-section');
            const appearanceResult = document.getElementById('appearance-result');

            // Clear previous content
            appearanceResult.innerHTML = '';

            if (data.error) {
                // Display the error message
                appearanceResult.innerHTML = `<p style="color: red;">${data.error}</p>`;
            } else {
                // Display each unique character name with their appearances
                appearanceResult.innerHTML = '<ul>';  // Start unordered list
                const uniqueCharacterData = new Map();
                data.forEach(instance => {
                    const name = instance.Name;
                    const appearances = instance.Appearances;
                    if (!uniqueCharacterData.has(name)) {
                        uniqueCharacterData.set(name, appearances);
                    }
                });
                uniqueCharacterData.forEach((appearances, name) => {
                    appearanceResult.innerHTML += `<li>${name} (${appearances})</li>`;
                });
                appearanceResult.innerHTML += '</ul>';  // End unordered list
            }

            // Always display the result section
            resultSection.style.display = 'block';
        })
        .catch(error => {
            console.error('Error:', error);
            const resultSection = document.getElementById('result-section');
            resultSection.style.display = 'block';
            const appearanceResult = document.getElementById('appearance-result');
            appearanceResult.innerHTML = `<p style="color: red;">An error occurred. Please try again.</p>`;
        });
}