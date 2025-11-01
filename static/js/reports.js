document.addEventListener('DOMContentLoaded', function() {
    loadUserStats();
    loadStockMovements();
    loadStockByCategory();
    loadRecentActivities();
});

function loadUserStats() {
    fetch('/reports/api/user_stats')
        .then(response => response.json())
        .then(data => {
            const ctx = document.getElementById('userStatsChart').getContext('2d');
            new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: ['Ativos', 'Inativos', 'Administradores'],
                    datasets: [{
                        label: 'Usuários',
                        data: [data.active, data.inactive, data.admins],
                        backgroundColor: [
                            'rgba(40, 167, 69, 0.8)',
                            'rgba(255, 193, 7, 0.8)',
                            'rgba(220, 53, 69, 0.8)'
                        ],
                        borderColor: [
                            'rgba(40, 167, 69, 1)',
                            'rgba(255, 193, 7, 1)',
                            'rgba(220, 53, 69, 1)'
                        ],
                        borderWidth: 2
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'bottom',
                        },
                        title: {
                            display: true,
                            text: `Total de Usuários: ${data.total}`
                        }
                    }
                }
            });
        })
        .catch(error => console.error('Error loading user stats:', error));
}

function loadStockMovements() {
    fetch('/reports/api/stock_movements')
        .then(response => response.json())
        .then(data => {
            const ctx = document.getElementById('stockMovementsChart').getContext('2d');
            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: data.labels,
                    datasets: [
                        {
                            label: 'Entradas',
                            data: data.entries,
                            borderColor: 'rgba(40, 167, 69, 1)',
                            backgroundColor: 'rgba(40, 167, 69, 0.2)',
                            tension: 0.4,
                            fill: true
                        },
                        {
                            label: 'Saídas',
                            data: data.exits,
                            borderColor: 'rgba(220, 53, 69, 1)',
                            backgroundColor: 'rgba(220, 53, 69, 0.2)',
                            tension: 0.4,
                            fill: true
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'top',
                        },
                        title: {
                            display: false
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            ticks: {
                                stepSize: 10
                            }
                        }
                    }
                }
            });
        })
        .catch(error => console.error('Error loading stock movements:', error));
}

function loadStockByCategory() {
    fetch('/reports/api/stock_by_category')
        .then(response => response.json())
        .then(data => {
            const ctx = document.getElementById('stockCategoryChart').getContext('2d');
            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: data.labels,
                    datasets: [{
                        label: 'Quantidade em Estoque',
                        data: data.data,
                        backgroundColor: [
                            'rgba(54, 162, 235, 0.8)',
                            'rgba(255, 99, 132, 0.8)',
                            'rgba(255, 206, 86, 0.8)',
                            'rgba(75, 192, 192, 0.8)',
                            'rgba(153, 102, 255, 0.8)',
                            'rgba(255, 159, 64, 0.8)'
                        ],
                        borderColor: [
                            'rgba(54, 162, 235, 1)',
                            'rgba(255, 99, 132, 1)',
                            'rgba(255, 206, 86, 1)',
                            'rgba(75, 192, 192, 1)',
                            'rgba(153, 102, 255, 1)',
                            'rgba(255, 159, 64, 1)'
                        ],
                        borderWidth: 2
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            display: false
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            ticks: {
                                stepSize: 20
                            }
                        }
                    }
                }
            });
        })
        .catch(error => console.error('Error loading stock by category:', error));
}

function loadRecentActivities() {
    fetch('/reports/api/recent_activities')
        .then(response => response.json())
        .then(data => {
            const tbody = document.querySelector('#activitiesTable tbody');
            tbody.innerHTML = '';
            
            data.forEach(activity => {
                const row = tbody.insertRow();
                
                let badgeClass = 'secondary';
                if (activity.type === 'Entrada') badgeClass = 'success';
                else if (activity.type === 'Saída') badgeClass = 'danger';
                else if (activity.type === 'Ajuste') badgeClass = 'warning';
                
                row.innerHTML = `
                    <td><span class="badge bg-${badgeClass}">${activity.type}</span></td>
                    <td>${activity.item}</td>
                    <td>${activity.quantity > 0 ? '+' : ''}${activity.quantity}</td>
                    <td>${activity.date}</td>
                `;
            });
        })
        .catch(error => console.error('Error loading recent activities:', error));
}
