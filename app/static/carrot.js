window.addEventListener('load', function() {
    var xhr = null;

    getXmlHttpRequestObject = function() {
        if (!xhr) {
            xhr = new XMLHttpRequest();
        }
        return xhr;
    };

    updateLiveData = function() {
        xhr = getXmlHttpRequestObject();
        xhr.onreadystatechange = evenHandler;
        xhr.open("GET", '/update_temp', true);
        xhr.send(null);
    };

    updateLiveData();

    function evenHandler() {
        if (xhr.readyState == 4 && xhr.status == 200) {
            var temp = document.getElementById("temp");
            var temperature = xhr.responseText;
            temperature = parseFloat(temperature).toFixed(2);
            temp.innerHTML = temperature + "°C";
        }
    }

    // SocketIO event listener to update the temperature value in real-time
    var socket = io.connect();
    socket.on('connect', function() {
        console.log('Socket connected');
    });
    socket.on('new_temperature', function(data) {
        var temperature = data.temperature;
        var temp = document.getElementById("temp");
        temperature = parseFloat(temperature).toFixed(2);
        temp.innerHTML = temperature + "%";
    });

});