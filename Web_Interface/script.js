////////////////////////////////
//1. How does a characters' identity influence their alignment(good, bad, neutral)?
////////////////////////////////

document.getElementById("character-search-form").addEventListener("submit", function (event) {
  event.preventDefault();
  const characterName = document.getElementById("character-name").value;
  
  // Make an API call to your Flask backend to analyze character alignment
  // Replace 'apiEndpoint' with the actual API endpoint you'll use
  fetch(`/api/character_alignment?name=${characterName}`)
      .then(response => response.json())
      .then(data => {
          const resultSection = document.getElementById("result-section");
          const alignmentResult = document.getElementById("alignment-result");
          
          if (data.alignment) {
              alignmentResult.textContent = `Alignment: ${data.alignment}`;
              resultSection.style.display = "block";
          } else {
              alignmentResult.textContent = "Character not found.";
              resultSection.style.display = "block";
          }
      })
      .catch(error => console.error(error));
});

////////////////////////////////
//2. How does the number of good vs bad characters changes over x period of years in both DC and Marvel?
////////////////////////////////

document.addEventListener("DOMContentLoaded", function () {
  const searchButton = document.getElementById("searchButton");
  searchButton.addEventListener("click", searchCharacters);
});

function searchCharacters() {
  const startYear = document.getElementById("startYear").value;
  const endYear = document.getElementById("endYear").value;

  // Perform input validation here

  // Make an API call to your Flask backend
  fetch(`/api/character-analysis?startYear=${startYear}&endYear=${endYear}`)
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

  // Create and append elements to resultContainer to display data
  // Example: Create a table, list, or charts to show the results
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
      const response = await fetch(`/api/compare_appearances_and_films=${characterName}`);
      const data = await response.json();

      // Clear previous results
      resultContainer.innerHTML = '';

      // Display the results
      if (data.error) {
          resultContainer.innerHTML = `<p>${data.error}</p>`;
      } else {
          resultContainer.innerHTML = `
              <p>Character: ${data.character}</p>
              <p>Number of Comic Appearances: ${data.comicAppearances}</p>
              <p>Number of Films: ${data.films}</p>
          `;
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

      // Make an API call to your Flask backend to get results
      try {
          const response = await fetch(`/api/mpa_rating_performance=${selectedRating}`);
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