
var IMP = window.IMP;
IMP.init("imp04843517");

async function get_user_data() {
    const user_id = document.getElementById("user_id").value
    var customer_uid = user_id + '_billing_key'
    IMP.request_pay({
        pg : 'kcp.A52CY',
        pay_method : 'card',
        merchant_uid: 'make_billing_key ' + new Date().toLocaleString(),
        customer_uid: customer_uid,
        name: '빌링키 발급',
        amount: 1,
        buyer_email: '',
        buyer_name:  user_id,
        buyer_tel: '',
        buyer_addr: '',
        buyer_postcode: ''
    }, async function (rsp) { // callback
        if (rsp.success) {
            const response = await fetch('http://127.0.0.1:8000/user/get_billing_key/', {
                headers:{
                    "Content-Type": "application/json"
                },
                method:'POST',
                body:JSON.stringify({
                    "user_id":user_id,
                    "billing_key":customer_uid
                })
            })
            var response_json = response.json()
            alert(response_json["message"])
        } else {
        }
    });
}
