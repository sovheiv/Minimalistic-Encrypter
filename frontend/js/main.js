const url = new URL('http://127.0.0.1:5000/encrypt')
var params = []


let input_key = document.getElementById('input_key');
input_key.addEventListener('input', onChange, true);
let input_text = document.getElementById('input_string');
input_text.addEventListener('input', onChange, true);


function onChange() {
    let text = document.getElementById('input_string').value
    let key = document.getElementById('input_key').value

    console.info(text, key);
    if (key && text) {
        console.info("1")

        params = [['text', text], ['key', key]]
        url.search = new URLSearchParams(params)

        send_request(url)
            .then(data => {
                if (data["success"] == true) {
                    console.log(data["result"])
                    hide_error()
                    show_result(data["result"])

                }
                else {

                    console.log(data["error_message"])
                    hide_result()
                    show_error(data["error_message"])

                }
            })

    }
    else {
        hide_result()
        hide_error()

    }
}
function send_request(backend_url) {
    return fetch(backend_url)
        .then(response => {
            return response.json()
        })
}

function show_error(error) {
    document.getElementById('error_label').innerHTML = error;
    document.getElementById("error_div").className = "";
}
function hide_error() {
    document.getElementById("error_div").className = "d-none";
}

function show_result(result) {
    document.getElementById('result_label').innerHTML = result;
    document.getElementById("result_div").className = "";
}
function hide_result() {
    document.getElementById("result_div").className = "d-none";
}

