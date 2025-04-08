document.addEventListener("DOMContentLoaded", async () => {
    const statisticsDiv = document.getElementById("statistics");
    const ctx = document.getElementById("dataChart").getContext("2d");
    statisticsDiv.innerHTML = "Chargement des données...";

    try {
        const response = await fetch("http://localhost:5001/process");

        if (!response.ok) {
            throw new Error("Erreur lors de la récupération des données");
        }

        const data = await response.json();
        const stats = data.stats;

        // Filtrer les colonnes avec des valeurs nulles ou N/A
        const validColumns = stats.columns.filter(col => {
            return stats.mean_values[col] !== null && stats.mean_values[col] !== undefined;
        });

        // Création du tableau pour afficher les statistiques
        statisticsDiv.innerHTML = `
            <h3>Statistiques des Données</h3>
            <table class="stats-table">
                <thead>
                    <tr>
                        <th>Colonnes</th>
                        <th>Moyenne</th>
                        <th>Valeur Maximale</th>
                        <th>Valeur Minimale</th>
                    </tr>
                </thead>
                <tbody>
                    ${validColumns.map((col) => {
                        return `
                            <tr>
                                <td>${col}</td>
                                <td>${stats.mean_values[col]?.toFixed(2) || "N/A"}</td>
                                <td>${stats.max_values[col]?.toFixed(2) || "N/A"}</td>
                                <td>${stats.min_values[col]?.toFixed(2) || "N/A"}</td>
                            </tr>
                        `;
                    }).join("")}
                    <tr>
                        <td><strong>Total des lignes</strong></td>
                        <td colspan="3">${stats.row_count}</td>
                    </tr>
                </tbody>
            </table>
        `;

        // Préparer les données pour le graphique
        const labels = validColumns;
        const meanValues = labels.map(col => stats.mean_values[col]);

        // Nettoyer le graphique précédent s’il existe
        if (window.myChart) window.myChart.destroy();

        window.myChart = new Chart(ctx, {
            type: "bar",
            data: {
                labels: labels,
                datasets: [{
                    label: "Moyennes des colonnes",
                    data: meanValues,
                    backgroundColor: "rgba(0, 255, 204, 0.3)",
                    borderColor: "rgba(0, 255, 204, 1)",
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        labels: {
                            color: "white"
                        },
                        position: "top"
                    },
                    title: {
                        display: true,
                        text: "Graphique des Moyennes",
                        color: "white",
                        font: {
                            size: 18
                        }
                    }
                },
                scales: {
                    x: {
                        ticks: {
                            color: "white"
                        }
                    },
                    y: {
                        ticks: {
                            color: "white"
                        }
                    }
                }
            }
        });
    } catch (error) {
        statisticsDiv.innerHTML = `<p style="color: red;">${error.message}</p>`;
    }
});

// Gestion du téléchargement du fichier CSV
document.getElementById("download-csv").addEventListener("click", () => {
    window.location.href = "http://localhost:5001/download";
});
