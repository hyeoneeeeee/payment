var IMP = window.IMP;
IMP.init("imp04843517");

async function requestPay() {
    var user_id = document.getElementById('user_id').value
    const response = await fetch("http://127.0.0.1:8000/usage/stop_charging/", {
        headers: {
            "Content-Type": "application/json",
        },
        method: 'POST',
        body:JSON.stringify({
            "user_id":user_id
        })
    })
    var response_json = await response.json()
    var merchant_uid = response_json["data"]["merchant_uid"]
    var name = response_json["data"]["name"]
    var amount = response_json["data"]["amount"]*1
    var buyer_name = response_json["data"]["buyer_name"]
    if (response_json["message"] == "결제필요"){

        IMP.request_pay({
            pg : 'kcp.A52CY',
            pay_method : 'card',
            merchant_uid: merchant_uid,
            name : name,
            amount : amount,
            buyer_email : '',
            buyer_name : buyer_name,
            buyer_tel : '',
            buyer_addr : '',
            buyer_postcode : ''
        }, async function (rsp) { // callback
            if (rsp.success) {
                const request = await fetch("http://127.0.0.1:8000/usage/stop_charging/", {
                    headers: {
                        "Content-Type": "application/json",
                    },
                    method: 'PUT',
                    body: JSON.stringify({
                        "imp_uid": rsp.imp_uid,
                        "merchant_uid": response_json["data"]["merchant_uid"],
                        "user_id":user_id
                    }),
                })
                var request_json = request.json()
                console.log(rsp);
                alert(rsp.error)
            } else {
                console.log(rsp);
                alert(rsp.error)
            }
        });
    }

}