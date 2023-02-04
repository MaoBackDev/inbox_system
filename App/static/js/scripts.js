// character reamining counter
$(document).ready(function (){
    let start = 0
    let limit = 1000

    $('#message').keyup(function() {
        start = this.value.length

        if(start > limit) {
            return false
        } 
        else if(start === 1000){
            $('#remaining').html(`Cracteres restantes ${limit - start}`).css('color', 'red')
            swal("Oops !", "Ha excedido el número de caracters !", "info")
        } 
        else if(start > 984){
            $('#remaining').html(`Cracteres restantes ${limit - start}`).css('color', 'red')
        } 
        else if(start < 1000){
            $('#remaining').html(`Cracteres restantes ${limit - start}`).css('color', 'black')
        } 
        else {
            $('#remaining').html(`Cracteres restantes ${limit}`).css('color', 'black')
        }
    })
})


// input mask (phone)
$(document).ready(function(){
    $('.phone').inputmask("999-999-9999", {'onincomplete': function(){
        swal("Opps !", "Teléfono incompleto. Por favor chequear", "info");
        $('.phone').val('')
        return false
    }})
})

// script to get the time running at realtime
setInterval(function() {
    let date = new Date()
    $('#clock').html(
        (date.getHours() < 10 ? '0': '') + date.getHours() + ':'+
        (date.getMinutes() < 10 ? '0': '') + date.getMinutes() + ':'+
        (date.getSeconds() < 10 ? '0': '') + date.getSeconds()
    )
}, 500)


// Script to update the page always at (0:00)
function autoRefresh(h, m, s) {
    let now = new Date()
    let then = new Date()

    then.setHours(h, m, s, 0)

    if(then.getTime() < now.getTime()){
        then.setDate(now.getDate() + 1)
    }
    let timeout = (then.getTime() - now.getTime())

    setTimeout(function() {
        window.location.reload(true)
    }, timeout)
}
autoRefresh(0, 0, 0)

// OCULTAR CONTENIDO DEL INBOX SI AL REALIZAR UN FILTRO NO HAY RESULTADOS
$(document).ready(function() {

    let verify = $('#check_td').length

    if (verify == 0){
        $('.hide').css('display', 'none')
        $('#msg').text('No hay resultados para la búsqueda')
        $('#refresh').html('<i class="bi bi-arrow-repeat"></i>')
    }
})

// SCRIPT PARA AVISAR AL USUARIO QUE EL SISTEMA CERRARÁ EN 5 MINUTOS
setTimeout(function(){
    let notice = document.querySelector('#warning')
    if(notice){
        notice.click()
    }
}, 25 * 60000)

// SCRIPT AUTO LOGOUT DESPUÉS QUE PASEN LOS 5 MINUTOS DEL AVISO
setTimeout(function(){
    let action = document.querySelector('#info')
    if(action){
        action.click()
    }
}, 30 * 60000)   // 30 min 60000 = 1 min



// FUNCTION TO SHOW PASSWORD
function myFunction() {
    let p = document.getElementById('password')
    if(p.type === 'password'){
        p.type = 'text'
    }else {
        p.type = 'password'
    }
}

