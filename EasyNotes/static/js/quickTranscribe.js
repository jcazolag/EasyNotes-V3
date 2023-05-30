const $transcribe_form = document.getElementById('Transcribe_form');
const $hidden = document.getElementById("hiddenResult");
const $audioName = document.getElementById("name");


const formData = new FormData();

window.addEventListener("load", async() =>{
    await cargaInicial();
});


const cargaInicial = async()=>{

    $transcribe_form.addEventListener('submit', llamarFuncion);

};

const llamarFuncion = async(e)=>{
    e.preventDefault();

    let file = document.forms['Transcribe_form']['audio_file'].files[0];

    if( !file ){
        notificacionSwal("Warning", "Select an audio file", "warning", "OK");      
    }else {
        formData.append("file", file);
        transcribir(e); 
        showLoading();   
    }
    

}



const transcribir = async(e)=>{
    try {
        const response=await fetch("/logic/whisper", {
            method: "post",
            body: formData,
        });

        const data=await response.json();
        
        if(data.mesage === "Success"){
            $audioName.value = data.name;
            $hidden.value = data.result;
            $transcribe_form.submit();
            return false;
        } else if (data.mesage === "Error") { 
            
            notificacionSwal('Error', "There was an error. Please try again", "error", "OK");
        }
    } catch (error) {
        console.log(error);
        notificacionSwal('Error', "There was an error. Please try again", "error", "OK");
    }
};


function fileValidation(){
    var fileInput = document.getElementById('audio_file');
    var filePath = fileInput.value;
    var allowedExtensions = /(.mp3|.mp4|.mpeg|.mpga|.m4a|.wav|.webm)$/i;
    if(!allowedExtensions.exec(filePath)){
        notificacionSwal('Warning','Please upload file having extensions mp3, mp4, mpeg, mpga, m4a, wav, or webm only.',"warning", "OK");
        fileInput.value = '';
        return false;
    }
}