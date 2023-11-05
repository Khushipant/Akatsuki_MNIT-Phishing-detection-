let isActive = false;

function checkURL(url) {
  if (isActive) {
    fetch('http://ffa3-35-221-24-41.ngrok-free.app/check_url', {
      method: 'POST',
      body: JSON.stringify({ url: url }),
      headers: {
        'Content-Type': 'application/json'
      }
    })
      .then(response => response.json())
      .then(data => {
        if (data.final_result === 0) {
          alert('This is a fraud site.');
        } else if (data.final_result === 1) {
          alert('This is a legit site.');
        }
      })
      .catch(error => console.error('Error:', error));
  }
}

document.addEventListener('mouseover', function (e) {
  if (e.target.tagName === 'A') {
    const url = e.target.href;
    setTimeout(() => {
      checkURL(url);
    }, 4000);
  }
});

chrome.browserAction.onClicked.addListener(function () {
  isActive = !isActive;
});
