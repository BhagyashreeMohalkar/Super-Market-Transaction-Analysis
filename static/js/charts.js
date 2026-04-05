window.onload = function() {

    new Chart(document.getElementById('ruleChart'), {
        type: 'bar',
        data: {
            labels: ruleLabels,
            datasets: [{
                label: 'Lift',
                data: ruleLifts,
                backgroundColor: '#2c5364'
            }]
        },
        options: {
            responsive: true
        }
    });

    new Chart(document.getElementById('timeChart'), {
        type: 'bar',
        data: {
            labels: ['Apriori', 'FP-Growth'],
            datasets: [{
                label: 'Execution Time (sec)',
                data: [aprioriTime, fpgrowthTime],
                backgroundColor: ['#203a43', '#00d4ff']
            }]
        }
    });
};