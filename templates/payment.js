
var IMP = window.IMP;
IMP.init("imp04843517");

async function requestPay() {
    const TIME_ZONE = 9 * 60 * 60 * 1000;
    const d = new Date('2021-08-05 09:51:31');
    const date = new Date(d.getTime() + TIME_ZONE).toISOString().split('T')[0];
    const time = d.toTimeString().split(' ')[0];
    const date_time = date + ' ' + time
    var user_id = document.getElementById("user_id").value

    const response = await fetch(`http://127.0.0.1:8000/payment/charging_point/?user_id=${user_id}`, {
        herders: {
            "Content-Type": "application/json",
        },
        method: 'GET'
    })

    var response_json = await response.json()
    var amount = document.getElementById("amount").value
    var merchant_uid = "merchant_" + new Date().getTime()
    const customer_uid = response_json["billing_key"]
    if (customer_uid == "") {

        IMP.request_pay({
            pg: 'kcp.A52CY',
            pay_method: 'card',
            merchant_uid: `${merchant_uid}`,
            name: '포인트 충전',
            amount: `${amount}`,
            buyer_email: '',
            buyer_name: user_id,
            buyer_tel: '',
            buyer_addr: '',
            buyer_postcode: ''
        }, async function (rsp) { // callback
            if (rsp.success) {
                const request = await fetch("http://127.0.0.1:8000/payment/charging_point/", {
                    headers: {
                        "Content-Type": "application/json",
                    },
                    method: 'POST',
                    body: JSON.stringify({
                        "buyer_name": user_id,
                        "amount": amount,
                        "payment_time": date_time,
                        "imp_uid": rsp.imp_uid,
                        "merchant_uid": merchant_uid,
                        "name": "포인트 충전"
                    }),
                })
                var request_json = request.json()
                alert(request_json["message"])
            } else {
                console.log(rsp);
            }
        });
    } else {
        const request = await fetch("http://127.0.0.1:8000/payment/charging_point/", {
            headers: {
                "Content-Type": "application/json",
            },
            method: 'POST',
            body: JSON.stringify({
                "buyer_name": user_id,
                "amount": amount,
                "customer_uid" :customer_uid,
                "payment_time": date_time,
                "merchant_uid": merchant_uid,
                "name": "포인트 충전"
            }),
        })
    }
}
