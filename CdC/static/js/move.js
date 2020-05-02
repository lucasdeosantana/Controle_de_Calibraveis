function change_retirada(valor, elemento) {
    document.getElementById(elemento).innerText = valor
    sendFormVisible()
}
function sendFormVisible() {
    dropdownretirada = document.getElementById("DropDownRetirada").innerText
    dropdownrecebido = document.getElementById("DropDownRecebido").innerText
    if (dropdownretirada != "Estação de Retirada" && dropdownrecebido != "Estação de Destino") {
        document.getElementById("enviarMovimentacao").style.display = ""
    }
}
function existEquipament() {
    alertclean()
    equipmentNumber = document.getElementById("equipamentData").value
    data = {
        "equipmentCode": equipmentNumber,
        "type": "request"
    }
    send_receive(data, "/move/")
}
function do_move() {
    equipmentNumber = document.getElementById("equipamentData").value
    where = document.getElementById("DropDownRetirada").innerText
    for_to = document.getElementById("DropDownRecebido").innerText
    data = {
        "type": "doMove",
        "equipmentCode": equipmentNumber,
        "where": where,
        "for": for_to
    }
    send_receive(data, "/move/")
}
var get_response = {
    EquipmentInformation(dict) {
        document.getElementById("DropDownRetirada").innerText = dict["in_station"]
        document.getElementById("equipmentName").innerText = dict["name"]
        document.getElementById("locations").style.display = ""
        document.getElementById("EquipamentName").style.display = ""
    },
    Success(dict) {
        var alert = document.getElementById("statusAlert")
        alertclean()
        alert.classList.add("alert-success")
        alert.innerText = "Movimentação Realizada com Sucesso"
        alert.style.display = ""
        document.getElementById("locations").style.display = "none"
        document.getElementById("EquipamentName").style.display = "none"
        document.getElementById("enviarMovimentacao").style.display = "none"
        document.getElementById("DropDownRecebido").innerText = "Estação de Destino"
    },
    Fail(dict) {
        var alert = document.getElementById("statusAlert")
        alertclean()
        alert.classList.add("alert-danger")
        alert.innerText = "Aconteceu Algum Problema"
        alert.style.display = ""
    },
    Warning(dict) {
        var alert = document.getElementById("statusAlert")
        alertclean()
        alert.classList.add("alert-warning")
        alert.innerText = "Equipamento Marcado para Calibração"
        alert.style.display = ""
    }
}
function alertclean() {
    var alert = document.getElementById("statusAlert")
    alert.classList.remove("alert-danger")
    alert.classList.remove("alert-sucess")
    alert.classList.remove("alert-warning")
    alert.style.display = "none"
}