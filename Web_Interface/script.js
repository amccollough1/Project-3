////////////////////////////////
//1. How does a characters' identity influence their alignment(good, bad, neutral)?
////////////////////////////////

document.getElementById("character-search-form").addEventListener("submit", function (event) {
    event.preventDefault();
    const characterName = document.getElementById("character-name").value;

    // Make an API call to  Flask backend to analyze character alignment
    fetch("#http://127.0.0.1:5000/api/character_identity_influence")
        .then(response => response.json())
        .then(data => {
            const resultSection = document.getElementById("result-section");
            const alignmentResult = document.getElementById("alignment-result");

            if (data.alignment) {
                alignmentResult.textContent = `Alignment: ${data.alignment}`;
                resultSection.style.display = "block";

                // Create a bar chart for alignment
                const ctx = document.getElementById("alignment-chart").getContext("2d");
                new Chart(ctx, {
                    type: "bar",
                    data: {
                        labels: ["Alignment"],
                        datasets: [
                            {
                                label: "Character Alignment",
                                data: [data.alignmentScore], //  need to define a score based on alignment
                                backgroundColor: "rgba(75, 192, 192, 0.2)",
                                borderColor: "rgba(75, 192, 192, 1)",
                                borderWidth: 1,
                            },
                        ],
                    },
                });

            } else {
                alignmentResult.textContent = "Character not found.";
                resultSection.style.display = "block";
            }
        });
});




////////////////////////////////
//2. How does the number of good vs bad characters changes over x period of years in both DC and Marvel?
////////////////////////////////

document.addEventListener("DOMContentLoaded", function () {
  const searchButton = document.getElementById("search-button");
  searchButton.addEventListener("click", searchCharacters);
});

function searchCharacters() {
  const startYear = document.getElementById("startYear").value;
  const endYear = document.getElementById("endYear").value;

  // Perform input validation
  if (!isValidYear(startYear) || !isValidYear(endYear)) {
    alert("Please enter valid start and end years.");
    return; // Exit the function if validation fails
}

  // Make an API call to your Flask backend
  fetch(`#http://127.0.0.1:5000/api/character_count_over_time?start_year=2000&end_year=&universe=both&alignment=Good`)
      .then(response => response.json())
      .then(data => {
          displayResults(data);
      })
      .catch(error => {
          console.error("Error fetching data:", error);
      });
}

function displayResults(data) {
    const resultContainer = document.getElementById("resultContainer");
    resultContainer.innerHTML = ""; // Clear previous results

    // Create a bar chart for good vs. bad characters over time
    const ctx = document.getElementById("character-count-chart").getContext("2d");
    new Chart(ctx, {
        type: "bar",
        data: {
            labels: data.years, // An array of years
            datasets: [
                {
                    label: "Good Characters",
                    data: data.goodCharacterCounts, // An array of counts
                    backgroundColor: "rgba(75, 192, 192, 0.2)",
                    borderColor: "rgba(75, 192, 192, 1)",
                    borderWidth: 1,
                },
                {
                    label: "Bad Characters",
                    data: data.badCharacterCounts, // An array of counts
                    backgroundColor: "rgba(255, 99, 132, 0.2)",
                    borderColor: "rgba(255, 99, 132, 1)",
                    borderWidth: 1,
                },
            ],
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true,
                },
            },
        },
    });
}


/////////////////////////////////////////
//3. How does the number of appearances in DC/Marvel comics compare to the films released?
////////////////////////////////////////

document.addEventListener('DOMContentLoaded', () => {
    const searchForm = document.getElementById('search-form');
    const resultContainer = document.getElementById('result-container');
  
    searchForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const characterName = document.getElementById('character-name').value;
        
        // Make an API call to your Flask backend
        const response = await fetch("#http://127.0.0.1:5000/api/character_count_over_time?start_year=2000&end_year=&universe=both&alignment=Good");
        const data = await response.json();
  
        // Clear previous results and chart
        resultContainer.innerHTML = '';
  
        // Display the results
        if (data.error) {
            resultContainer.innerHTML = `<p>${data.error}</p>`;
        } else {
            resultContainer.innerHTML = `
                <p>Character: ${data.character}</p>
                <p>Number of Comic Appearances: ${data.comicAppearances}</p>
                <p>Number of Films: ${data.films}</p>
                <canvas id="bar-chart"></canvas> <!-- Add a canvas for the bar chart -->
            `;

            // Create a bar chart
            const ctx = document.getElementById('bar-chart').getContext('2d');
            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: ['Comic Appearances', 'Films'],
                    datasets: [{
                        label: 'Counts',
                        data: [data.comicAppearances, data.films],
                        backgroundColor: ['rgba(75, 192, 192, 0.2)', 'rgba(255, 99, 132, 0.2)'],
                        borderColor: ['rgba(75, 192, 192, 1)', 'rgba(255, 99, 132, 1)'],
                        borderWidth: 1,
                    }]
                },
                options: {
                    scales: {
                        y: {
                            beginAtZero: true,
                        },
                    },
                },
            });
        }
    });
});



////////////////////////////////////
//4. Film Release : Is there a particular MPA rating that performs better over another?
///////////////////////////////////

document.addEventListener("DOMContentLoaded", function () {
  const searchButton = document.getElementById("search-button");
  const mpaRatingSelect = document.getElementById("mpa-rating");
  const resultsContainer = document.querySelector(".results");

  searchButton.addEventListener("click", async () => {
      const selectedRating = mpaRatingSelect.value;

      // Make an API call to Flask backend to get results
      try {
          const response = await fetch("@app.route('/api/mpa_rating_performance', methods=['GET'])\n");
          if (!response.ok) {
              throw new Error(`HTTP Error! Status: ${response.status}`);
          }

          const data = await response.json();

          // Clear previous results
          resultsContainer.innerHTML = "";

          // Display the results
          data.forEach((film) => {
              const filmCard = document.createElement("div");
              filmCard.classList.add("film-card");
              filmCard.innerHTML = `
                  <h2>${film.title}</h2>
                  <p>Release Date: ${film.releaseDate}</p>
                  <p>Box Office: $${film.boxOffice}</p>
              `;
              resultsContainer.appendChild(filmCard);
          });
      } catch (error) {
          console.error("Error:", error);
      }
  });
});