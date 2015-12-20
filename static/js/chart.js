function lineChartHandler(data) {
    $(function () {
        $('#container').highcharts({
            title: {
                text: 'The most popular words of reddit.api',
                x: -20 //center
            },
            xAxis: {
                categories: data['popular_words']
            },
            yAxis: {
                plotLines: [{
                    value: 0,
                    width: 1,
                    color: '#808080'
                }]
            },
            legend: {
                layout: 'vertical',
                align: 'right',
                verticalAlign: 'middle',
                borderWidth: 0
            },
            series: data['words_info']
        });
    });
}

function barChartHandler(data) {
    var mainChartData = [];
    var drilldownData = [];
    _.each(data, function(item){
        mainChartData.push({
            'name': item['name'],
            'y': item['subscribers'],
            'drilldown': item['name']
        });
        drilldownData.push({
            'name': item['name'],
            'id': item['name'],
            'data': item['words']
        })
    });
    $(function () {
        // Create the chart
        $('#container').highcharts({
            chart: {
                type: 'column'
            },
            title: {
                text: 'Popular subreddits of the day and popular words for them'
            },
            subtitle: {
                text: 'Click the columns to popular words of subreddit.</a>.'
            },
            xAxis: {
                type: 'category'
            },
            yAxis: {
                title: {
                    text: 'Subreddit subscribers'
                }

            },
            legend: {
                enabled: false
            },
            plotOptions: {
                series: {
                    borderWidth: 0,
                    dataLabels: {
                        enabled: true,
                        format: '{point.y}'
                    }
                }
            },

            tooltip: {
                headerFormat: '<span style="font-size:11px">{series.name}</span><br>',
                pointFormat: '<span style="color:{point.color}">{point.name}</span>: <b>{point.y}</b> subscribers<br/>'
            },

            series: [{
                name: 'Brands',
                colorByPoint: true,
                data: mainChartData
            }],
            drilldown: {
                xAxis: {
                    type: 'Words'
                },
                yAxis: {
                    title: {
                        text: 'Count'
                    }

                },
                plotOptions: {
                    series: {
                        borderWidth: 0,
                        dataLabels: {
                            enabled: true,
                            format: '{point.y}'
                        }
                    }
                },
                series: drilldownData
            }
        });
    });
}