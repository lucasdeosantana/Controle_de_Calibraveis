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
function transfer(destiny, equipmentNumber) {
    data = {
        "type": "doMove",
        "equipmentCode": equipmentNumber,
        "where": "{{ where }}",
        "for": destiny
    }
    send_receive(data)
}
var get_response = {
    EquipmentInformation(dict) {

    },
    Success(dict) {
        document.getElementById(dict["equipmentCode"]).outerHTML = "";
    },
    Fail(dict) {

    },
    Warning(dict) {

    }
}
