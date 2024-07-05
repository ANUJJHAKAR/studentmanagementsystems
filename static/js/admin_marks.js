// Define the subject codes for each semester
const subjects = {
    "I": ["CSE101", "CSE102", "CSE103", "CSE104", "CSE105"],
    "II": ["CSE201", "CSE202", "CSE203", "CSE204", "CSE205"],
    "III": ["CSE301", "CSE302", "CSE303", "CSE304", "CSE305"],
    "IV": ["CSE401", "CSE402", "CSE403", "CSE404", "CSE405"],
    "V": ["CSE501", "CSE502", "CSE503", "CSE504", "CSE505"],
    "VI": ["CSE601", "CSE602", "CSE603", "CSE604", "CSE605"]
};

// Function to update the table based on the selected semester
function updateTable() {
    const semester = document.getElementById("semester").value;
    const tableBody = document.getElementById("marks-table-body");

    // Update selected semester display
    document.getElementById('selected-semester').textContent = semester;

    // Clear the current table body
    tableBody.innerHTML = "";

    // Get the subjects for the selected semester
    const selectedSubjects = subjects[semester];
    
    // Create table rows for each subject
    selectedSubjects.forEach(subject => {
        const row = document.createElement("tr");
        
        // Subject code cell
        const subjectCell = document.createElement("td");
        subjectCell.textContent = subject;
        row.appendChild(subjectCell);
        
        // Marks input cell
        const marksCell = document.createElement("td");
        const marksInput = document.createElement("input");
        marksInput.type = "number";
        marksInput.min = 0;
        marksInput.max = 100;
        marksInput.name = `marks_${subject}`;
        marksCell.appendChild(marksInput);
        row.appendChild(marksCell);
        
        // Append the row to the table body
        tableBody.appendChild(row);
    });
}

// Function to handle the upload button click (you can expand this to include actual upload logic)
function uploadMarks() {
    // Get all the input fields
    const inputs = document.querySelectorAll('input[type="number"]');
    const enrollmentInputs = document.querySelectorAll('input[type="text"]');

    // Validate each input
    for (let input of inputs) {
        const value = Number(input.value);
        if (isNaN(value) || value < 0 || value > 100) {
            alert("Invalid input: " + input.name);
            return;
        }
    }

    for (let input of enrollmentInputs) {
        const value = input.value;
        if (!/^\d{9}$/.test(value)) {
            alert("Invalid enrollment number: " + value);
            return;
        }
    }

    // If all inputs are valid, continue with the upload
    alert("Marks uploaded!");
}
