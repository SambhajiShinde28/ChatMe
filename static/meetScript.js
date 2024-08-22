
var container = document.getElementsByClassName("display-container")[0];
container.style.height = window.screen.height - 100 + "px"



var copyGroupCode = document.getElementById('copy-group-code')

copyGroupCode.addEventListener('click', () => {
    var inputField = document.getElementById('code-share-input')
    inputField.select();
    inputField.setSelectionRange(0, 99999);
    document.execCommand('copy');
})




var usernameValidation = document.getElementById('use-name-validation')
var groupnameValidation = document.getElementById('groupName-validation')

var sendMsgBtn = document.getElementById('msg-send-bn')
var msg = document.getElementById('send-message-input')

var display_msg = document.getElementsByClassName('display-messages-container')[0]



if (usernameValidation.value != "" && groupnameValidation.value != "") {

    var ws = new WebSocket("ws://127.0.0.1:8000/chatme/" + groupnameValidation.value + "/" + usernameValidation.value)

    ws.onopen = (e) => {
        console.log("Connection open", e)
    }

    var file_upload=document.getElementById('file-upload')
    file_upload.addEventListener('change',()=>{
        alert("This feature did not activate till, It will come soon !!")
    })

    var exitBtn = document.getElementsByClassName('exitBtn')[0]
    exitBtn.addEventListener('click', () => {
        document.getElementsByClassName('connected-people-list')[0].innerHTML = ''
        document.getElementsByClassName('connected-people-list')[1].innerHTML = ''
        display_msg.innerHTML=''
        ws.close(1000, 'Normal closure')
    })


    sendMsgBtn.addEventListener('click', () => {

        display_msg.insertAdjacentHTML('beforeend', '<div class="dummy-diplay-person-send-message"><div class="diplay-person-send-message"><p class="send-person-name">' + usernameValidation.value + ' (Me)</p><p class="send-person-message">' + msg.value + '</p></div></div>')

        ws.send(JSON.stringify({
            'usename': usernameValidation.value,
            'code': groupnameValidation.value,
            'msg': msg.value,
            'requestType': 'chat message'
        }))

        msg.value = ""
    })


    ws.onmessage = (e) => {

        if (JSON.parse(e.data).requestType == 'chat message') {

            if (msg.value != JSON.parse(e.data).msg && JSON.parse(e.data).msg != 'none') {
                if (usernameValidation.value != JSON.parse(e.data).usename) {
                    display_msg.insertAdjacentHTML('beforeend', '<div class="dummy-diplay-person-receive-message"><div class="diplay-person-receive-message"><p class="receive-person-name">' + JSON.parse(e.data).usename + '</p><p class="receive-person-message">' + JSON.parse(e.data).msg + '</p></div></div>')
                }
            }
        }

        else if (JSON.parse(e.data).requestType == 'no of user diaplay') {

            if (Object.values(JSON.parse(e.data).Yes) != '' && JSON.parse(e.data).adminRequest == 'none') {

                document.getElementsByClassName('connected-people-list')[0].innerHTML = ''
                document.getElementsByClassName('connected-people-list')[1].innerHTML = ''

                try {
                    var users = Object.values(JSON.parse(e.data).Yes)
                    var disusers = Object.values(JSON.parse(e.data).No)
                } catch (error) { }

                try {
                    users.forEach(e => {
                        document.getElementsByClassName('connected-people-list')[0].insertAdjacentHTML('beforeend', '<li class="list-group-item d-flex justify-content-between align-items-start users" style="background-color: transparent !important;"><div class="ms-2 me-auto"><div class="fw-bold">' + e + '</div></div><span class="badge text-bg-primary rounded-pill">.</span></li>')
                    });
                } catch (error) { }

                try {
                    disusers.forEach(e => {
                        document.getElementsByClassName('connected-people-list')[1].insertAdjacentHTML('beforeend', '<li class="list-group-item d-flex justify-content-between align-items-start users" style="background-color: transparent !important;"><div class="ms-2 me-auto"><div class="fw-bold">' + e + '</div></div></li>')
                    });
                } catch (error) { }

            }
        }

        else if (JSON.parse(e.data).requestType == 'Previous Chat Of Group') {

            var chat = JSON.parse(e.data).previousData
            chat.forEach((e)=>{
                
                if (usernameValidation.value == e.name) {
                    display_msg.insertAdjacentHTML('beforeend', '<div class="dummy-diplay-person-send-message"><div class="diplay-person-send-message"><p class="send-person-name">' + e.name + ' (Me)</p><p class="send-person-message">' + e.message + '</p></div></div>')
                }
                else{
                    display_msg.insertAdjacentHTML('beforeend', '<div class="dummy-diplay-person-receive-message"><div class="diplay-person-receive-message"><p class="receive-person-name">' + e.name + '</p><p class="receive-person-message">' + e.message + '</p></div></div>')
                }

            })
        }

    }

    ws.onerror = (e) => {
        console.log("Connection error : ", e)
    }

    ws.onclose = (e) => {
        console.log("Connection closed : ", e)
    }

}
else {
    alert("You are Unauthorized User !!")
}






