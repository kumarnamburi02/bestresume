// Function to navigate to the analyze page when the button is clicked
function goToAnalyzePage() {
  window.location.href = '/analyze'; // Redirect to the "/analyze" page
}

// Add a click event listener to the "Analyze the Resume" button
document.getElementById('analyze-btn').addEventListener('click', goToAnalyzePage);

function uploadFile(inputName) {
  const inputElement = document.getElementById(inputName);
  const file = inputElement.files[0];
  const formData = new FormData();
  formData.append(inputName, file);

  fetch('/upload', {
    method: 'POST',
    body: formData
  })
  .then(response => response.json())
  .then(data => {
    console.log(data);
  })
  .catch(error => {
    console.error('Error:', error);
  });
}

function analyzeResume() {
  const jobDescriptionFile = document.getElementById('job-description').files[0];
  const resumeFile = document.getElementById('resume').files[0];
  
  const formData = new FormData();
  formData.append('job-description', jobDescriptionFile);
  formData.append('resume', resumeFile);

  fetch('/analyze', {
    method: 'POST',
    body: formData
  })
  .then(response => response.json())
  .then(data => {
    const percentageResultElement = document.getElementById('percentage-result');
    if (data.hasOwnProperty('error')) {
      percentageResultElement.textContent = `Error: ${data.error}`;
    } else if (data.hasOwnProperty('matching_percentage')) {
      percentageResultElement.textContent = `Percentage of matching keywords: ${data.matching_percentage.toFixed(2)}%`;
    } else {
      percentageResultElement.textContent = 'Error: Unable to calculate matching percentage';
    }
  })
  .catch(error => {
    console.error('Error:',error);
  });
}