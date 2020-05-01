function send_receive(dictonary) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var response = JSON.parse(this.responseText)
            get_response[response["type"]](response)
        }
    }
    jsonString = JSON.stringify(dictonary)
    xhttp.open("POST", '/move/')
    xhttp.setRequestHeader("Content-Type", "application/json")
    xhttp.send(jsonString)
}
var get_response = {}