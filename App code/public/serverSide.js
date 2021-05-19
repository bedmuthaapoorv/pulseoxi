function get(){
    axios({
        "method": "GET",
        "url": "https://api.thingspeak.com/channels/1045791/feeds.json?api_key=Z7GLYGYG00M4DKOJ&results=1"
    }).then(response => {
        updateData(response.data);
    });
    axios({
        "method": "GET",
        "url": "https://api.apify.com/v2/key-value-stores/toDWvRj1JpTXiM8FF/records/LATEST?disableRedirect=true"
    }).then(response1 => {
        updateCovid(response1);
    });
}
setInterval(get,2000);
var Readings;
function updateData(abc){
//console.log(abc);
TSresponse=abc.feeds[0].field1;
Readings=TSresponse.split(",");//[11.6,22]
    document.getElementById("bpm").innerHTML=Math.ceil(Readings[0]);
    document.getElementById("o2").innerHTML=Math.ceil(Math.abs(Readings[1]));
    age=document.getElementById("age").innerHTML;
    document.getElementById("actualHR").innerHTML=Math.ceil(Math.ceil(Readings[0])*100/(220-age));
    document.getElementById("expectedHR").innerHTML=64;
    
}
function updateCovid(response1){
    //console.log(response1.data.regionData[20]);
    document.getElementById("totalInf").innerHTML=(response1.data.regionData[20].totalInfected);
    document.getElementById("newInf").innerHTML=Math.abs(response1.data.regionData[20].newInfected);

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
function validate(){
    users=["apoorv"]
    pass=["apoorv"]
    u=document.getElementById("username").value;
    p=document.getElementById("password").value;
    if(u=="apoorv"){
        if(p=="apoorv"){
            location.replace("Home.html");
        }
    }
    else{
        location.replace("https://www.w3schools.com")
    }

}
finalJSON={0:[]}
function LabelEncoding(i){
j=(""+i["date_died"]).split('-')
const date1=new Date('1/1/2020')
const date2=new Date(j[2],j[1],j[0])
dates=(date2-date1)/100000
console.log(i["sex"])
ActualElement=[
parseInt(i["sex"]),
parseInt(i["pneumonia"]),
parseInt(i["asthma"]),
parseInt(i["cardiovascular"]),
parseInt(i["copd"]),
parseInt(i["covid_res"]),
parseInt(dates),
parseInt(i["diabetes"]),
parseInt(i["hypertension"]),
parseInt(i["icu"]),
parseInt(i["intubed"]),
parseInt(i["obesity"]),
parseInt(i["other_disease"]),
parseInt(i["pneumonia"]),
parseInt(i["pregnency"]),
parseInt(i["renal_chronic"]),
parseInt(i["sex"]),
parseInt(i["tobacco"])
]
console.log(ActualElement)
}
function FeatureEngineering(dataframe){
indexList=[1,7,8,9,6,10,11,12,14,15,16,17,18,19,21,22,5]
for(let j=1;j<50000;j++){
    element={}
    for(let i=0;i<this.indexList.length;i++){
        element[dataframe[0][this.indexList[i]]]=dataframe[j][this.indexList[i]];
    }    
finalJSON[0].push(element)
}
LabelEncoding(finalJSON[0][5])
console.log(finalJSON)
}
function runner(i){

    let csv = Papa.parse(i,{ 
        delimiter: "", // auto-detect 
        newline: "", // auto-detect 
        quoteChar: '"', 
        escapeChar: '"', 
        header: false, // creates array of {head:value} 
        dynamicTyping: false, // convert values to numbers if possible
        skipEmptyLines: true 
      }); 
      FeatureEngineering(csv.data);

}
function loadDoc() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
        runner(this.responseText);
      }
    };
    xhttp.open("GET", "covid.csv", true);
    xhttp.send();
  }
loadDoc();