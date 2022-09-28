


function ServerAPI_RAW_POST(data, resultfunc, resultfuncparam)
{

    //console.log(new Error().stack);

    var startTime = null;

    $.ajax({
        type: 'POST',
        dataType: 'json',
        data: JSON.stringify(data),
        beforeSend: function () {
            startTime = new Date();
            },
        success: function (data) {
            var timeDiff = (new Date()) - startTime;
            console.log('AJAX :  success, ' + timeDiff.toString()+' ms');
            if ((!data.iserror) && (resultfunc != null))
                resultfunc(resultfuncparam,data);

        },
        error: function (req, status, error) {
            var timeDiff = (new Date()) - startTime;
            console.log('AJAX : ' + status + ', ' + error + ', ' + timeDiff.toString() + ' ms');
            if (resultfunc != null)
                resultfunc(null);
        }
    });

}  
	
    
    
function ServerAPI(indata,resultfunc)
{
    ServerAPI_RAW_POST(indata, resultfunc, indata);
}