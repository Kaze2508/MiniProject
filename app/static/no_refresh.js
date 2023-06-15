window.addEventListener('load', function()
{
    var xhr = null;
    getXmlHttpRequestObject = function()
    {
        if(!xhr)
        {               
            xhr = new XMLHttpRequest();
        }
        return xhr;
    };

    updateLiveData = function()
    {
            xhr = getXmlHttpRequestObject();
            xhr.onreadystatechange = evenHandler;
            xhr.open("GET", '/my_route', true);
            xhr.send(null);
    };

    // updateLiveData = function()
    // {
    //     var now = new Date();
    //     var url = '/static/livefeed.txt?' + now.getTime();
    //     xhr = getXmlHttpRequestObject();
    //     xhr.onreadystatechange = evenHandler;
    //     xhr.open("GET", url, true);
    //     xhr.send(null);
    // };

    updateLiveData();

    function evenHandler()
    {
        // Check response is ready or not
        if(xhr.readyState == 4 && xhr.status == 200)
        {
            table = document.getElementById("myTable");
            dData = xhr.responseText;            
            // var tbody = table.getElementsByTagName("tbody")[0];
            // tbody.innerHTML = "";
            table.innerHTML = dData;
            // var rows = tbody.getElementsByTagName("tr");
            // for (var i = 0; i < rows.length; i++) 
            // {
            //     tbody.removeChild(rows[i]);
            // }
            // for (var i = 0; i < dData.length; i++) 
            // {
            //     var row = tbody.insertRow();
            //     var idCell = row.insertCell(0);
            //     var topicCell = row.insertCell(1);
            //     var payloadCell = row.insertCell(2);
            //     idCell.innerHTML = dData[i].id;
            //     topicCell.innerHTML = dData[i].topic;
            //     payloadCell.innerHTML = dData[i].payload;
            // }
            setTimeout(updateLiveData(), 1000);
        }
    }
});