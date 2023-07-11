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
        xhr.open("GET", '/update_humi', true);
        xhr.send(null);
    };

    updateLiveData();

    function evenHandler() {
        if (xhr.readyState == 4 && xhr.status == 200) {
            var humi = document.getElementById("hum");
            var temperature = xhr.responseText;
            humidity = parseFloat(humidity).toFixed(2);
            humi.innerHTML = humidity + "°C";
        }
    }

    // SocketIO event listener to update the temperature value in real-time
    var socket = io.connect();
    socket.on('connect', function() {
        console.log('Socket connected');
    });
    socket.on('new_humidity', function(data) {
        var humidity = data.humidity;
        var humi = document.getElementById("hum");
        humidity = parseFloat(humidity).toFixed(2);
        humi.innerHTML = humidity + "%";
    });

});