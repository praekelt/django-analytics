function requestData_{{ object.id }}() {
    $.ajax({
        url: '{% url highcharts_data object.id %}',
        success: function(point) {
            $.each(point, function(index) {
                var series = chart_{{ object.id }}.series[index],
                    shift = series.data.length > {{ object.samples }}; // shift if the series is longer required samples
                    chart_{{ object.id }}.series[index].addPoint(point[index], false, shift);
            });
                
            setTimeout(requestData_{{ object.id }}, 1000);    
            chart_{{ object.id }}.redraw()    
        },
        cache: false
    });
}
