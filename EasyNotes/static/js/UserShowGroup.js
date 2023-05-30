const $update_form = document.getElementById('update_group_form');
const $delete_form = document.getElementById('delete_group_form');
const $group_title = document.getElementById('group_title');
const $group_id = document.getElementById('group_id')


const UpdateData = new FormData();

window.addEventListener("load", async() =>{
    await cargaInicial();
});

const cargaInicial = async()=>{

    $update_form.addEventListener('submit', update);
    $delete_form.addEventListener('submit', Delete);

};

const update = async(event)=>{
    event.preventDefault();
    try {
        if( $group_title.value < 1){
            notificacionSwal("Warning", "The title cannot be empty", "warning", "OK");      
        }else {
            UpdateData.append("group_id", $group_id.value);
            UpdateData.append("group_title", $group_title.value);
            const csrftoken = Cookies.get('csrftoken');
            const response=await fetch("/user/update/", {
                method: "post",
                body: UpdateData,
                mode: 'same-origin',
                headers: {'X-CSRFToken': csrftoken}
            }); 
            const data=await response.json();

            if(data.message === "Success"){
                var url = '/user/group/'
                var form = $('<form action="' + url + '" method="post">' +
                '<input type="hidden" name="csrfmiddlewaretoken" value="' + csrftoken + '" />'+
                '<input type="hidden" name="group_id" value="' + $group_id.value + '" />' +
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
          $delete_form.submit();
        }
      })
}