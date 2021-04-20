function get(){
    axios({
        "method": "GET",
        "url": "https://api.thingspeak.com/channels/1045791/feeds.json?api_key=Z7GLYGYG00M4DKOJ&results=1"
    }).then(response => {
        updateData(response.data);
    });
}
function updateData(abc){
console.log(abc);
TSresponse=abc.feeds[0].field1;
Readings=TSresponse.split(",");
    document.getElementById("bpm").innerHTML=Math.ceil(Readings[0]);
    document.getElementById("o2").innerHTML=Math.ceil(Readings[1]);
}