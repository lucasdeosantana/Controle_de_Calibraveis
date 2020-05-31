document.querySelector("button[type='submit']").addEventListener('click',
        ()=>{
            event.preventDefault()
            let form=document.querySelector("form")
            let formValues={payload:{}, type:"createCar"}
            for(let index=0;index<form.elements.length-1; index++){
                if(form.elements[index].type != "checkbox"){
                    formValues.payload[form.elements[index].name]=form.elements[index].value
                }else{
                    formValues.payload[form.elements[index].name]=form.elements[index].checked
                }
            }
            send_receive(formValues, ajaxurl)
        })
var get_response={
    createCar(response){
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
            alertFrame.innerText="Usuario Criado com Sucesso"
            document.querySelector("form").reset()
        }else{
            alertFrame.setAttribute('class',"alert alert-danger")
            alertFrame.innerText="Houve Algum erro"
        }
        alertFrame.appendChild(iconbuttonAlert)
        noticeFrame.appendChild(alertFrame)
    }
}