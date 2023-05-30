const $update_form = document.getElementById('update_note_form');
const $delete_form = document.getElementById('delete_note_form');
const $date_form = document.getElementById('date_note_form');
const $summary_form = document.getElementById('summary_note_form');
const $study_material_form = document.getElementById('study_material_note_form');



const $note_title = document.getElementById('note_title');
const $note_text = document.getElementById('note_text');
const $note_id = document.getElementById('note_id')
const $link_back = document.getElementById('link_back')
const $group_id = document.getElementById('group_id')


const UpdateData = new FormData();
const deleteData = new FormData();

const actionData = new FormData();

const dateData = new FormData();
const summaryData = new FormData();
const study_materialData = new FormData();

window.addEventListener("load", async() =>{
    await cargaInicial();
});

const cargaInicial = async()=>{

    $update_form.addEventListener('submit', update);
    $delete_form.addEventListener('submit', Delete);

    $summary_form.addEventListener('submit', summary);
    $date_form.addEventListener('submit', date);
    $study_material_form.addEventListener('submit', study_material);

    $link_back.addEventListener('click', go_back)

};

const update = async(event)=>{
    event.preventDefault();
    try {
        if( $note_title.value < 1){
            notificacionSwal("Warning", "The title cannot be empty", "warning", "OK");      
        }else {
            UpdateData.append("note_id", $note_id.value);
            UpdateData.append("note_title", $note_title.value);
            UpdateData.append("note_text", $note_text.value);
            const csrftoken = Cookies.get('csrftoken');
            const response=await fetch("/user/update/", {
                method: "post",
                body: UpdateData,
                mode: 'same-origin',
                headers: {'X-CSRFToken': csrftoken}
            }); 
            const data=await response.json();

            if(data.message === "Success"){
                var url = '/user/note/'
                var form = $('<form action="' + url + '" method="post">' +
                '<input type="hidden" name="csrfmiddlewaretoken" value="' + csrftoken + '" />'+
                '<input type="hidden" name="note_id" value="' + $note_id.value + '" />' +
                '</form>');
                $('body').append(form);
                form.submit();
            } else if (data.message === "Error") { 

                notificacionSwal('Error', data.error, "error", "OK");
            }
        }
    } catch (error) {
        console.log(error);
        notificacionSwal('Error', error, "error", "OK");
    } 

}

const Delete = async(event)=>{
    event.preventDefault();
    Swal.fire({
        title: 'Are you sure?',
        text: "You won't be able to revert this!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Yes, delete it!'
      }).then((result) => {
        if (result.isConfirmed) {
            Delete_get();
        }
      })
}

const summary = async(event)=>{
    event.preventDefault();
    try {

        actionData.append("note_id", $note_id.value);
        actionData.append("option", 'summary');
        const csrftoken = Cookies.get('csrftoken');
        showLoading();
        const response=await fetch("/logic/chat", {
            method: "post",
            body: actionData,
            mode: 'same-origin',
            headers: {'X-CSRFToken': csrftoken}
        });
        
        const data=await response.json();
        
        if(data.mesage === "Success"){
            console.log("Success logic")
            summaryData.append("note_id", $note_id.value);
            summaryData.append("result", data.result);
            summaryData.append("option", 'summary');
            const csrftoken = Cookies.get('csrftoken');
            
            const response=await fetch("/user/create/", {
                method: "post",
                body: summaryData,
                mode: 'same-origin',
                headers: {'X-CSRFToken': csrftoken}
            });
            showLoading();
            const summary_data = await response.json();
            if(summary_data.message === "Success"){
                var url = '/user/note/'
                var form = $('<form action="' + url + '" method="post">' +
                '<input type="hidden" name="csrfmiddlewaretoken" value="' + csrftoken + '" />'+
                '<input type="hidden" name="note_id" value="' + $note_id.value + '" />' +
                '</form>');
                $('body').append(form);
                form.submit();
            } else if (summary_data.message === "Error") {  
                notificacionSwal('Error', "There was an error. Please try again", "error", "OK");
            }else if (summary_data.message === "False"){
                notificacionSwal('Error', "Wrong parameters", "error", "OK");
            }
        } else if (data.mesage === "Error") { 
            notificacionSwal('Error', "There was an error. Please try again", "error", "OK");
        }
    } catch (error) {
        console.log(error);
        notificacionSwal('Error', "There was an error. Please try again", "error", "OK");
    }
}

const date = async(event)=>{
    event.preventDefault();
    try {

        actionData.append("note_id", $note_id.value);
        actionData.append("option", 'date');
        const csrftoken = Cookies.get('csrftoken');
        showLoading();
        const response=await fetch("/logic/chat", {
            method: "post",
            body: actionData,
            mode: 'same-origin',
            headers: {'X-CSRFToken': csrftoken}
        });
        
        const data=await response.json();
        
        if(data.mesage === "Success"){
            dateData.append("note_id", $note_id.value);
            dateData.append("result", data.result);
            dateData.append("option", 'date');
            const csrftoken = Cookies.get('csrftoken');
            
            const response=await fetch("/user/create/", {
                method: "post",
                body: dateData,
                mode: 'same-origin',
                headers: {'X-CSRFToken': csrftoken}
            });
            showLoading();
            const date_data = await response.json();
            if(date_data.message === "Success"){
                var url = '/user/note/'
                var form = $('<form action="' + url + '" method="post">' +
                '<input type="hidden" name="csrfmiddlewaretoken" value="' + csrftoken + '" />'+
                '<input type="hidden" name="note_id" value="' + $note_id.value + '" />' +
                '</form>');
                $('body').append(form);
                form.submit();
            } else if (date_data.message === "Error") {  
                notificacionSwal('Error', "There was an error. Please try again", "error", "OK");
            }else if (date_data.message === "False"){
                notificacionSwal('Error', "Wrong parameters", "error", "OK");
            }
        } else if (data.mesage === "Error") { 
            notificacionSwal('Error', "There was an error. Please try again", "error", "OK");
        }
    } catch (error) {
        console.log(error);
        notificacionSwal('Error', "There was an error. Please try again", "error", "OK");
    }
}

const study_material = async(event)=>{
    event.preventDefault();
    try {

        actionData.append("note_id", $note_id.value);
        actionData.append("option", 'study_material');
        const csrftoken = Cookies.get('csrftoken');
        showLoading();
        const response=await fetch("/logic/chat", {
            method: "post",
            body: actionData,
            mode: 'same-origin',
            headers: {'X-CSRFToken': csrftoken}
        });
        
        const data=await response.json();
        
        if(data.mesage === "Success"){
            study_materialData.append("note_id", $note_id.value);
            study_materialData.append("result", data.result);
            study_materialData.append("option", 'study_material');
            const csrftoken = Cookies.get('csrftoken');
            showLoading();
            const response=await fetch("/user/create/", {
                method: "post",
                body: study_materialData,
                mode: 'same-origin',
                headers: {'X-CSRFToken': csrftoken}
            });
            
            const study_material_data = await response.json();
            if(study_material_data.message === "Success"){
                var url = '/user/note/'
                var form = $('<form action="' + url + '" method="post">' +
                '<input type="hidden" name="csrfmiddlewaretoken" value="' + csrftoken + '" />'+
                '<input type="hidden" name="note_id" value="' + $note_id.value + '" />' +
                '</form>');
                $('body').append(form);
                form.submit();
            } else if (study_material_data.message === "Error") {  
                notificacionSwal('Error', "There was an error. Please try again", "error", "OK");
            }else if (study_material_data.message === "False"){
                notificacionSwal('Error', "Wrong parameters", "error", "OK");
            }
        } else if (data.mesage === "Error") { 
            notificacionSwal('Error', "There was an error. Please try again", "error", "OK");
        }
    } catch (error) {
        console.log(error);
        notificacionSwal('Error', "There was an error. Please try again", "error", "OK");
    }
}

const Delete_get = async()=>{
    try {
        deleteData.append("note_id", $note_id.value);
        const csrftoken = Cookies.get('csrftoken');
        const response=await fetch("/user/delete/", {
            method: "post",
            body: deleteData,
            mode: 'same-origin',
            headers: {'X-CSRFToken': csrftoken}
        }); 
        const data=await response.json();

        if(data.message === "Success"){
            var url = '/user/group/'
            var form = $('<form action="' + url + '" method="post">' +
            '<input type="hidden" name="csrfmiddlewaretoken" value="' + csrftoken + '" />'+
            '<input type="hidden" name="group_id" value="' + data.group_id + '" />' +
            '</form>');
            $('body').append(form);
            form.submit();
        }
    } catch (error) {
        console.log(error);
        notificacionSwal('Error', error, "error", "OK");
    } 
}

const go_back = (event)=>{
    event.preventDefault()
    try {
        const csrftoken = Cookies.get('csrftoken');
        var url = '/user/group/'
        var form = $('<form action="' + url + '" method="post">' +
        '<input type="hidden" name="csrfmiddlewaretoken" value="' + csrftoken + '" />'+
        '<input type="hidden" name="group_id" value="' + $group_id.value + '" />' +
        '</form>');
        $('body').append(form);
        form.submit();
    } catch (error) {
        console.log(error)
    }
    
}