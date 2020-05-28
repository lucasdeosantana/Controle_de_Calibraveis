function transfer(destiny, equipmentNumber) {
    where = document.title
    data={
        "type": "doMove",
        "equipmentCode": equipmentNumber,
        "where": where,
        "for": destiny
    }
    send_receive(data, "/move/")
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
