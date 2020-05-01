var get_response = {
    requestTemplate(dict){

    }
}
function changecarfree(){
    document.getElementById("cars_inuse").classList.remove("active")
    document.getElementById("cars_free").classList.add("active")
    document.getElementById("cars_free_table").style.display=""
    document.getElementById("cars_inuse_table").style.display="none"
    data={
        "type":"requestTemplate",
        "args":["cars_free"]
    }
    send_receive(data, "/cars/")
}
function changecarinuse(){
    document.getElementById("cars_free").classList.remove("active")
    document.getElementById("cars_inuse").classList.add("active")
    document.getElementById("cars_free_table").style.display="none"
    document.getElementById("cars_inuse_table").style.display=""
    data={
        "type":"requestTemplate",
        "args":["cars_inuse"]
    }
    send_receive(data, "/cars/")
}