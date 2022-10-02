// co:here mail classifier
function coherePostal() {
  const warning = document.querySelector('#warning');
  const mailSubject = document.querySelector('#subject').value;
  const mailBody = document.querySelector('#body').value;
  const mailLabel = document.querySelector('input[name=mailLabel]');
  if (mailSubject == "") {
    warning.innerHTML = "Mail Subject need value.";
  }
  if (mailBody == "") {
    warning.innerHTML = "Mail Body need value.";
  }
   (async () => {
      mailLabel.value = "...";
      const response = await fetch('/api/cohere/postal', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({subject: mailSubject, body: mailBody})
      })
      .then((response) => response.json())
      .then((data) => {
        console.log("Request:", {subject: mailSubject, body: mailBody});
        console.log("Response:", data);
        warning.innerHTML = 'Open console log for request & response data.';  
        if (data.success) {
          mailLabel.value = data.prediction;
        } else {
          mailLabel.value = "error";
        }
      });
    })();
  
  return;
};
