document.querySelector("#search").addEventListener('click',()=>{
    let inputCode=document.querySelector('[aria-describedby="search"]')
    let Payload={license:inputCode.value}
    let data={
        type:"search",
        payload:Payload

    }
    send_receive(data, ajaxurl)
})
document.querySelector('#deleteModalButton').addEventListener('click', ()=>{
    document.querySelector('#labelModalTitle').innerText=`Delete Car License: ${document.querySelector('[name="license"]').value}`
})

document.querySelector('#deleteAnyway').addEventListener('click',()=>{
    let Payload={
        license:document.querySelector('[name="license"]').value
    }
    let data = {
        type:"deletecar",
        payload: Payload
    }
    send_receive(data, ajaxurl)
})
function createalert(response, Message){
    let noticeFrame = document.querySelector(".notice")
    noticeFrame.innerHTML=""
    let alertFrame = document.createElement('div')
    let iconbuttonAlert = document.createElement('i')
    alertFrame.style.display="flex"
    alertFrame.style.justifyContent="space-between"
    alertFrame.style.alignItems="center"
    alertFrame.style.position="absolute"
    alertFrame.style.width="30%"
    alertFrame.style.zIndex="2"
    alertFrame.style.marginTop="10px"
    alertFrame.setAttribute('role','alert')
    iconbuttonAlert.setAttribute('class','fas fa-times')
    iconbuttonAlert.style.cursor="pointer"
    iconbuttonAlert.addEventListener('click',()=>{
        noticeFrame.innerHTML=""
    })
    if(response.status == "success"){
        alertFrame.setAttribute('class',"alert alert-success")
        alertFrame.innerText=Message
    }else{
        alertFrame.setAttribute('class',"alert alert-danger")
        alertFrame.innerText="There was an error"
    }
    alertFrame.appendChild(iconbuttonAlert)
    noticeFrame.appendChild(alertFrame) 
}
var get_response ={
    search(response){
        if(response.status == "success"){
            let fields = JSON.parse(response.payload)[0].fields
            document.querySelector('[name="name"]').value = fields.name
            document.querySelector('[name="isactive"]').checked=fields.is_active
            document.querySelector("#send").addEventListener("click",()=>{
                event.preventDefault()
                let Payload={license:document.querySelector('[name="license"]').value}
                let form=document.querySelector(".root")
                for(let i=0; i<form.length-1; i++){
                    if(form[i].type!='checkbox'){
                        Payload[form[i].name]=form[i].value
                    }else{
                        Payload[form[i].name]=form[i].checked
                    }
                }
                let data = {
                    type:"editcar",
                    payload:Payload
                }
                send_receive(data, ajaxurl)
            })
            document.querySelector(".root").style.display=""
        }else{
            createalert(response)
        }
    },
    editcar(response){
        createalert(response, "Car was edit with success")
        document.querySelector(".root").style.display="none"
    },
    deletecar(response){
        createalert(response, "Car was delete!")
        document.querySelector('[data-dismiss="modal"]').click()
        document.querySelector(".root").style.display="none"
    }
        
}