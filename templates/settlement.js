


async function get_user_data() {
    var user_id = document.getElementById('user_id').value
    const response = await fetch("http://127.0.0.1:8000/usage/stop_charging/", {
        headers: {
            "Content-Type": "application/json",
        },
        method: 'POST',
        body: JSON.stringify({
            "user_id": user_id
        })
    })
    var response_json = await response.json()
    merchant_uid = response_json["data"]["merchant_uid"]
    response_name = response_json["data"]["name"]
    amount = response_json["data"]["amount"]
    buyer_name = response_json["data"]["buyer_name"]
    if (response_json["message"] == '결제필요') {
        alert('결제시작')
        requestPay()
    } else {
        alert(request_json["message"])
    }
}
var IMP = window.IMP;
IMP.init("imp04843517");

function requestPay() {
    IMP.request_pay({
        pg: 'kcp',
        pay_method: 'card',
        merchant_uid: merchant_uid,
        name: response_name,
        amount: amount,
        buyer_email: '',
        buyer_name: buyer_name,
        buyer_tel: '',
        buyer_addr: '',
        buyer_postcode: ''
    }, function (rsp) { // callback
        if (rsp.success) {
            const request = fetch("http://127.0.0.1:8000/usage/stop_charging/", {
                headers: {
                    "Content-Type": "application/json",
                },
                method: 'PUT',
                body: JSON.stringify({
                    "imp_uid": rsp.imp_uid,
                    "merchant_uid": merchant_uid,
                    "user_id": user_id
                })
            })
            console.log(rsp);
        } else {
            console.log(rsp);
        }
    });
}