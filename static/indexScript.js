var newMeeting = document.getElementsByClassName("option-btn")[0]
var joinMeeting = document.getElementsByClassName("option-btn")[1]

var newGroupContainer = document.getElementsByClassName('new-meeting')[0]
var joinGroupContainer = document.getElementsByClassName('join-meeting')[0]

var startBtn = document.getElementsByClassName('start-btn')[0]
var joinBtn = document.getElementsByClassName('join-btn')[0]

var userName = document.getElementById('user-name')
var code = document.getElementById('code')
var joinUserName = document.getElementById('join-user-name')

var csrf = document.getElementById('csrf_value').getAttribute('value')


newMeeting.addEventListener("click", () => {
    newGroupContainer.style.display = 'block'
    joinGroupContainer.style.display = 'none'
})

joinMeeting.addEventListener('click', () => {
    newGroupContainer.style.display = 'none'
    joinGroupContainer.style.display = 'block'
})


startBtn.addEventListener("click", () => {
    if (userName.value != '') {

        var formData = new FormData()
        formData.append('user-name', userName.value)
        formData.append('user-type', "New-Group")

        var xhr = new XMLHttpRequest()

        xhr.open('POST', 'http://127.0.0.1:8000/group', true)

        xhr.onload = function () {
            if (xhr.status >= 200 && xhr.status < 300) {
                try {
                    var response = JSON.parse(xhr.responseText);

                    if (response.result == "Completed9f8") {
                        window.open('http://127.0.0.1:8000/live', target = "_self")
                    }

                    else if(response.result == 'EmptyFieldsj78n'){
                        alert('User-Name is empty !!')
                    }

                    else {
                        alert("Something Went Wrong !!")
                    }
                }
                catch (error) { }
            }
            else {
                console.error('Error : ' + xhr.status);
            }
        };

        xhr.setRequestHeader('X-CSRFToken', csrf);

        xhr.send(formData)

    }
    else {
        document.getElementsByClassName('start-btn')[0].style.marginTop = '0px'
        document.getElementsByClassName('warning')[0].style.display = 'block'
        document.getElementsByClassName('warning')[0].innerText = "Name Field Is Empty"
    }
})

joinBtn.addEventListener("click", () => {
    if (joinUserName.value != '') {

        if (code.value != '') {

            var formData = new FormData()
            formData.append('join-user-name', joinUserName.value)
            formData.append('meeting-code', code.value)
            formData.append('user-type', "Existing-Group")

            var xhr = new XMLHttpRequest()

            xhr.open('POST', 'http://127.0.0.1:8000/group', true)

            xhr.onload = function () {
                if (xhr.status >= 200 && xhr.status < 300) {
                    try {
                        var response = JSON.parse(xhr.responseText);
                    
                        if (response.result == "Completed9f8") {
                            window.open('http://127.0.0.1:8000/live', target = "_self")
                        }

                        else if(response.result == 'CodeFailj9z39e'){
                            alert("Invalid Group Code !!")
                        }

                        else if(response.result == 'EmptyFieldsj78n'){
                            alert('User-Name & Group-Code is empty !!')
                        }

                        else {
                            alert("Something Went Wrong !!")
                        }
                    }
                    catch (error) { }
                }
                else {
                    console.error('Error : ' + xhr.status);
                }
            };

            xhr.setRequestHeader('X-CSRFToken', csrf);

            xhr.send(formData)

        }
        else {
            document.getElementsByClassName('join-btn')[0].style.marginTop = '0px'
            document.getElementsByClassName('warning')[2].style.display = 'block'
            document.getElementsByClassName('warning')[2].innerText = "Group-Code Is Empty"
        }

    }
    else {
        code.style.marginBottom = "20px"
        joinUserName.style.marginBottom = "0px"
        document.getElementsByClassName('join-btn')[0].style.marginTop = '0px'
        document.getElementsByClassName('warning')[1].style.display = 'block'
        document.getElementsByClassName('warning')[1].innerText = "User-Name Is Empty"
    }
})