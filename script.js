document.addEventListener('DOMContentLoaded', () => {
    fetch('condutas.json')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            const patientList = document.getElementById('patient-list');
            if (!patientList) return;

            data.forEach(patient => {
                const card = document.createElement('div');
                card.className = 'patient-card';

                const title = document.createElement('h2');
                title.textContent = patient.paciente;
                card.appendChild(title);

                const todoList = document.createElement('ul');
                todoList.className = 'todo-list';

                patient.condutas.forEach(itemText => {
                    const listItem = document.createElement('li');
                    listItem.textContent = itemText;
                    
                    // Add toggle functionality for completed status
                    listItem.addEventListener('click', () => {
                        listItem.classList.toggle('completed');
                    });

                    todoList.appendChild(listItem);
                });

                card.appendChild(todoList);
                patientList.appendChild(card);
            });
        })
        .catch(error => {
            console.error('Error fetching or parsing condutas.json:', error);
            const patientList = document.getElementById('patient-list');
            if (patientList) {
                patientList.innerHTML = '<p style="color: red;">Could not load patient data. Please check the console for errors.</p>';
            }
        });
});
