$(function() {
	var day_data = [
	    {
            "fecha": '2015-01-28',
            "Temperatura": 2,
			"TempMax": 3,
			"TempMin": 1,
            "TempMed": 2,
            
        },{
            "fecha": '2015-01-29',
            "Temperatura": 5,
			"TempMax": 8,
			"TempMin": 3,
            "TempMed": 4,
            
        },{
            "fecha": '2015-01-30',
            "Temperatura": 2,
			"TempMax": 7,
			"TempMin": 0,
            "TempMed": 5,
            
        },{
            "fecha": '2015-01-31',
            "Temperatura": 4,
			"TempMax": 10,
			"TempMin": 5,
            "TempMed": 5,
            
        },
		{
            "fecha": '2015-02-01',
            "Temperatura": 15,
			"TempMax": 20,
			"TempMin": 10,
            "TempMed": 15,
            
        }];
    Morris.Line({
        element: 'morris-area-chart',
        data: day_data,
        xkey: 'fecha',
        ykeys: ['Temperatura', 'TempMax', 'TempMin','TempMed'],
        labels: ['Temperatura', 'TempMax', 'TempMin','TempMed'],
        resize: true
    });

    Morris.Donut({
        element: 'morris-donut-chart',
        data: [{
            label: "Download Sales",
            value: 12
        }, {
            label: "In-Store Sales",
            value: 30
        }, {
            label: "Mail-Order Sales",
            value: 20
        }],
        resize: true
    });

    Morris.Bar({
        element: 'morris-bar-chart',
        data: [{
            y: '2006',
            a: 100,
            b: 90
        }, {
            y: '2007',
            a: 75,
            b: 65
        }, {
            y: '2008',
            a: 50,
            b: 40
        }, {
            y: '2009',
            a: 75,
            b: 65
        }, {
            y: '2010',
            a: 50,
            b: 40
        }, {
            y: '2011',
            a: 75,
            b: 65
        }, {
            y: '2012',
            a: 100,
            b: 90
        }],
        xkey: 'y',
        ykeys: ['a', 'b'],
        labels: ['Series A', 'Series B'],
        hideHover: 'auto',
        resize: true
    });

});
