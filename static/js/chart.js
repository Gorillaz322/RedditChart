function chartHandler2(data) {
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