import $ from 'jquery';
import Chart from 'chart.js';

$(() => {
    const $soilMoistureChart = $('#soilMoistureChart');
    $.ajax({
        url: $soilMoistureChart.data('url'),
        success: (data) => {
            const ctx = $soilMoistureChart[0].getContext('2d');
            const white = 'rgba(255, 255, 255, 1)';
            const transparentWhite = 'rgba(255, 255, 255, 0.2)';
            const green = 'rgb(32, 201, 151, 1)';
            const transparentGreen = 'rgb(32, 201, 151, 0.2)';

            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: data.labels,
                    datasets: [
                        {
                            data: data.data,
                            backgroundColor: transparentGreen,
                            borderColor: green,
                            pointBackgroundColor: green,
                            pointHoverBorderWidth: 2,
                        },
                    ],
                },
                options: {
                    scales: {
                        yAxes: [
                            {
                                gridLines: {
                                    color: transparentWhite,
                                },
                                ticks: {
                                    beginAtZero: true,
                                    stepSize: 10,
                                    max: 100,
                                    fontColor: white,
                                    fontSize: 14,
                                    padding: 2,
                                    callback: (value) => value + '%',
                                },
                            },
                        ],
                        xAxes: [
                            {
                                type: 'time',
                                time: {
                                    unit: 'hour',
                                },
                                gridLines: {
                                    color: transparentWhite,
                                },
                                ticks: {
                                    maxTicksLimit: 12,
                                    fontColor: white,
                                    fontSize: 14,
                                    padding: 2,
                                },
                            },
                        ],
                    },
                    responsive: true,
                    legend: {
                        display: false,
                    },
                    title: {
                        display: true,
                        text: 'Soil Moisture',
                        fontSize: 20,
                        fontColor: white,
                    },
                    tooltips: {
                        mode: 'index',
                        intersect: false,
                        callbacks: {
                            title: (item, value) => moment(item[0].xLabel).format('h:mm a'),
                            label: (item, value) => item.value + '%',
                        },
                    },
                    hover: {
                        mode: 'index',
                        intersect: false,
                    },
                },
            });
        },
    });
});
