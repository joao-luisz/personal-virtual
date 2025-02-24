document.getElementById('preferences-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const muscleGroup = document.getElementById('muscle-group').value;
    const equipment = document.getElementById('equipment').value;

    const response = await fetch('https://seu_usuario.pythonanywhere.com/recommend', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ muscle_group: muscleGroup, equipment: equipment })
    });

    const recommendations = await response.json();
    const recommendationsDiv = document.getElementById('recommendations');
    if (recommendations.message) {
        recommendationsDiv.innerHTML = '<h2>Nenhum exercício encontrado</h2>';
    } else {
        recommendationsDiv.innerHTML = '<h2>Exercícios Recomendados:</h2>';
        recommendations.forEach(exercise => {
            recommendationsDiv.innerHTML += `<p>${exercise.Title} (${exercise.Equipment})</p>`;
        });
    }
});
