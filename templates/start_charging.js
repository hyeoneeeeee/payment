

async function requestCharge() {
    var user_id = document.getElementById('user_id').value
    const response = await fetch(`http://127.0.0.1:8000/usage/start_charging/?user_id=${user_id}`,{
        headers:{
            "Content-Type": "application/json",
        },
        method:'POST'
        })
    const response_json = await response.json()
    alert(response_json["message"])

}
