chart_{{ object.id }} = new Highcharts.Chart({
    chart: {
        renderTo: 'gadget{{ object.id }}',
        defaultSeriesType: 'spline',
        events: {
            load: requestData_{{ object.id }}
        }
    },
    title: {
        text: '{{ object }}'
    },
    xAxis: {
	    type: 'datetime',
		tickPixelInterval: 150,
		maxZoom: 20 * 1000,
		title: {
		    text: 'Date',
			margin: 10
		}
	},
	yAxis: {
	    minPadding: 0.2,
		maxPadding: 0.2,
		title: {
		    text: 'Value',
			margin: 10
		}
    },
    series: [
    {% for stat in object.stats %} 
        {
            name: '{{ stat }}',
			data: []
        },
    {% endfor %}
    ]
});
