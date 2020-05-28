var get_response = {
    requestTemplate(dict){
    template_renew[dict["args"][0]](dict)        
    },
    get_car(dict){
        if(dict["status"]=="success"){
            document.getElementById(dict["args"][0]).innerHTML=""
        }
    },
    set_car(dict){
        console.log(dict)
        if(dict["status"]=="success"){
            document.getElementById(dict["args"][1]).innerHTML=""
        }
    }
}
var template_renew = {
    cars_free(dict){
        document.getElementById("cars_free_body").innerHTML=dict["payloadHTML"]
    },
    cars_inuse(dict){
        document.getElementById("cars_inuse_body").innerHTML=dict["payloadHTML"]
    }
}
function changecarfree(){
    document.getElementById("cars_inuse").classList.remove("active")
    document.getElementById("cars_free").classList.add("active")
    document.getElementById("cars_free_table").style.display=""
    document.getElementById("cars_inuse_table").style.display="none"
    document.getElementById("cars_free_body").innerHTML=""
    document.getElementById("cars_inuse_body").innerHTML=""
    data={
        "type":"requestTemplate",
        "args":["cars_free"]
    }
    send_receive(data, "/CARS/")
}
function changecarinuse(){
    document.getElementById("cars_free").classList.remove("active")
    document.getElementById("cars_inuse").classList.add("active")
    document.getElementById("cars_free_table").style.display="none"
    document.getElementById("cars_inuse_table").style.display=""
    document.getElementById("cars_free_body").innerHTML=""
    document.getElementById("cars_inuse_body").innerHTML=""
    data={
        "type":"requestTemplate",
        "args":["cars_inuse"]
    }
    send_receive(data, "/CARS/")
}
function get_car(license_plate){
    data = {
        "type":"get_car",
        "args":[license_plate]
    }
    send_receive(data, "/CARS/")
}
function back_car(destiny, license_plate){
    data = {
        "type":"set_car",
        "args":[destiny, license_plate]
    }
    send_receive(data, "/CARS/")
}