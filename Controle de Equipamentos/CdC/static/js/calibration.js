function send_receive(dictonary) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var response = JSON.parse(this.responseText)
            console.log(response)
            get_response[response["type"]](response)
        }
    }
    jsonString = JSON.stringify(dictonary)
    xhttp.open("POST", '/super/Calibration/')
    xhttp.setRequestHeader("Content-Type", "application/json")
    xhttp.send(jsonString)
}
function changetab1() {
    document.getElementById("ER").classList.remove("active")
    document.getElementById("RE").classList.add("active")
    document.getElementById("equip_confirm_table").style.display = ""
    document.getElementById("equip_back_table").style.display = "none"
    document.getElementById("equip_confirm").innerHTML = ""
    document.getElementById("equip_back").innerHTML = ""
    data = {
        "type": "equipConfirm"
    }
    send_receive(data)
}
function changetab2() {
    document.getElementById("RE").classList.remove("active")
    document.getElementById("ER").classList.add("active")
    document.getElementById("equip_confirm_table").style.display = "none"
    document.getElementById("equip_back_table").style.display = ""
    document.getElementById("equip_confirm").innerHTML = ""
    document.getElementById("equip_back").innerHTML = ""
    data = {
        "type": "equipBack"
    }
    send_receive(data)

}
var get_response = {
    equipConfirm(dict) {
        document.getElementById("equip_confirm").innerHTML = dict["payload"]
    },
    equipBack(dict) {
        document.getElementById("equip_back").innerHTML = dict["payload"]
    },
    to_confirm(dict) {
        if (dict["payload"] == "Success") {
            document.getElementById(dict["code"]).innerHTML = ""
        }
    },
    to_cancel(dict) {
        if (dict["payload"] == "Success") {
            document.getElementById(dict["code"]).innerHTML = ""
        }
    },
    to_return(dict) {
        if (dict["payload"] == "Success") {
            document.getElementById(dict["code"]).innerHTML = ""
        }
    },
}
function button_received(code, type) {
    button_functs[type](code)
}
var button_functs = {
    btn_confirm(code) {
        data = {
            "type": "to_confirm",
            "code": code
        }
        send_receive(data)
    },
    btn_cancel(code) {
        data = {
            "type": "to_cancel",
            "code": code
        }
        send_receive(data)
    },
    btn_return(code) {
        data = {
            "type": "to_return",
            "code": code,
            "date": document.getElementById("d" + code.toString()).value

        }
        send_receive(data)
    }
}  