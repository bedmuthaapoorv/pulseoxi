function get(){
    axios({
        "method": "GET",
        "url": "https://api.thingspeak.com/channels/1045791/feeds.json?api_key=Z7GLYGYG00M4DKOJ&results=1"
    }).then(response => {
        updateData(response.data);
    });
}
var Readings;
function updateData(abc){
console.log(abc);
TSresponse=abc.feeds[0].field1;
Readings=TSresponse.split(",");
    document.getElementById("bpm").innerHTML=Math.ceil(Readings[0]);
    document.getElementById("o2").innerHTML=Math.ceil(Math.abs(Readings[1]));
    age=document.getElementById("age").innerHTML;
    document.getElementById("actualHR").innerHTML=Math.ceil(Math.ceil(Readings[0])*100/(220-age));
    document.getElementById("expectedHR").innerHTML=64;
    
}
function sendMessage(){
    
    content="hello the patient needs your attention,his current health is critical,BPM="+Readings[0]+" SP02="+Readings[1];
    var xhr = new XMLHttpRequest(),
    body = JSON.stringify(
        {
            "messages": [
                {
                    "channel": "sms",
                    "to": "919561295237",
                    "content": content
                },
            ]
        }
    );
    xhr.open('POST', 'https://platform.clickatell.com/v1/message', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.setRequestHeader('Authorization', 'ylxBmcz4TQSWpcB-ISzkdA==');
    xhr.onreadystatechange = function(){
        if (xhr.readyState == 4 && xhr.status == 200) {
            console.log('success');
        }
    };
    
    xhr.send(body)
    alert("Message Sent")    
}