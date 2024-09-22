function logoutClick() {
    window.location.href = "/logout";
}

function backClick() {
    window.location.href = "/fir";
}

function historyOpen(){
    window.location.href = "/details";
}

var Fid = undefined;

function addWitnessFeild() {
    var witness = document.getElementById("witness-inputs");    
    var newElement = document.createElement("div");
    newElement.innerHTML = `
        <div style="margin-top: 20px">
        <label for="witnessName">Name:</label>
        <input type="text" id="witnessName" name="witnessName[]" placeholder="Enter witness's name">
        </div>
    `;
    witness.appendChild(newElement);
}

function addAccusedFeild() {
    var accused = document.getElementById("accused-inputs");    
    var newElement = document.createElement("div");
    newElement.innerHTML = `
        <div style="margin-top: 20px">
        <label for="accusedName">Name:</label>
        <input type="text" id="accusedName" name="accusedName[]" placeholder="Enter accused's name">
        </div>
    `;
    accused.appendChild(newElement);
}

// document.addEventListener("DOMContentLoaded", function() {
function idleSave(){
    let timeout;
    const idleTime = 30000; // 30 seconds

    function resetTimer() {
        clearTimeout(timeout);
        timeout = setTimeout(sendIdleNotification, idleTime);
    }

    function sendIdleNotification() {
        // Get form values and replace empty fields with '-'
        const name = document.getElementById('name').value || '-';
        const fatherOrHusbandName = document.getElementById('fatherOrHusbandName').value || '-';
        const address = document.getElementById('address').value || '-';
        const phoneNumber = document.getElementById('phoneNumber').value || '-';
        const email = document.getElementById('email').value || '-';
    
        // Place of Occurrence
        const distanceFromPoliceStation = document.getElementById('distanceFromPoliceStation').value || '-';
        const directionFromPoliceStation = document.getElementById('directionFromPoliceStation').value || '-';
        const dateAndHourOfOccurrence = document.getElementById('dateAndHourOfOccurrence').value || '-';
    
        // Offence Details
        const natureOfOffence = document.getElementById('natureOfOffence').value || '-';
    
        // Stolen Property Description (optional, array)
        const stolenPropertyDescriptions = document.getElementById('stolenPropertyDescription').value || '-';
        
        // Accused Names (optional, array)
        const accusedInputs = document.querySelectorAll('[name="accusedName[]"]');
        const accusedNames = Array.from(accusedInputs).map(input => input.value || '-');
    
        // Witness Names (optional, array)
        const witnessInputs = document.querySelectorAll('[name="witnessName[]"]');
        const witnessNames = Array.from(witnessInputs).map(input => input.value || '-');
        
        // Complaint Text
        const complaint = document.getElementById('complaint').value || '-';
    
        // Construct the single-level JSON body
        const bodyData = {
            name: name,
            fatherOrHusbandName: fatherOrHusbandName,
            address: address,
            phoneNumber: phoneNumber,
            email: email,
            distanceFromPoliceStation: distanceFromPoliceStation,
            directionFromPoliceStation: directionFromPoliceStation,
            dateAndHourOfOccurrence: dateAndHourOfOccurrence,
            natureOfOffence: natureOfOffence,
            stolenPropertyDescriptions: stolenPropertyDescriptions,  // flat array
            accusedNames: accusedNames,                              // flat array
            witnessNames: witnessNames,                              // flat array
            complaint: complaint,
            id: Fid
        };
    
        // Make the POST request
        fetch('/firIntermediate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(bodyData)  // Send the form data as JSON
        })
        .then(response => {
            if (response.ok) {
                return response.json().then(dat => {
                    Fid = dat.id;
                    console.log(dat, "done here with intermediate fir");
                    return dat;
                });
            }
            throw new Error('Network response was not ok.');
        })
        .then(data => {
            console.log('Data sent successfully:', data);
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
        });
    }

    document.querySelectorAll('input').forEach(input => {
        input.addEventListener('input', resetTimer);
    });

    resetTimer();
// });
}
