axios({
    "method": "GET",
    "url": "https://api.apify.com/v2/key-value-stores/toDWvRj1JpTXiM8FF/records/LATEST?disableRedirect=true"
}).then(response1 => {
    updateCovid(response1);
});
function get(){
    axios({
        "method": "GET",
        "url": "https://api.thingspeak.com/channels/1045791/feeds.json?api_key=Z7GLYGYG00M4DKOJ&results=1"
    }).then(response => {
        updateData(response.data);
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
    age=document.getElementById("age").value;
    document.getElementById("actualHR").innerHTML=Math.ceil(Math.ceil(Readings[0])*100/(220-age));
    document.getElementById("expectedHR").innerHTML=64;
    
}
function updateCovid(response1){
    console.log(response1.data.regionData[20]);
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
ActualArray=[]

finalJSON={0:[]}
function predictor(){
    m=document.getElementById("male").checked;
    f=document.getElementById("female").checked;
    sex=1
    if(m==true){
        sex=2
    }
    else{
        sex=1
    }
    c=document.getElementById("pneumonia").checked;
    pneumonia=2
    if(c==true){
        pneumonia=1
    }
    else{
        pneumonia=2
    }
    c=document.getElementById("asthma").checked;
    ast=2
    if(c==true){
        ast=1
    }
    else{
        ast=2
    }
    c=document.getElementById("cardio").checked;
    cardio=2
    if(c==true){
        cardio=1
    }
    else{
        cardio=2
    }
    c=document.getElementById("copd").checked;
    copd=2
    if(c==true){
        copd=1
    }
    c=document.getElementById("diabetes").checked;
    dia=2
    if(c==true){
        dia=1
    }
    c=document.getElementById("hypertension").checked;
    hyp=2
    if(c==true){
        hyp=1
    }
    c=document.getElementById("icu").checked;
    icu=2
    if(c==true){
        icu=1
    }
    c=document.getElementById("intubed").checked;
    intubed=2
    if(c==true){
        intubed=1
    }
    c=document.getElementById("obesity").checked;
    obesity=2
    if(c==true){
        obesity=1
    }
    c=document.getElementById("other").checked;
    other=2
    if(c==true){
        other=1
    }
    c=document.getElementById("pregnency").checked;
    preg=2
    if(c==true){
        preg=1
    }
    c=document.getElementById("renal").checked;
    renal=2
    if(c==true){
        renal=1
    }
    c=document.getElementById("tobacco").checked;
    tob=2
    if(c==true){
        tob=1
    }
    testArr=[sex,pneumonia,ast,cardio,copd,2,0,dia,hyp,icu,intubed,obesity,other,preg,renal,tob]
    console.log(testArr)
    printer(testArr)
    
}
function LabelEncoding(i){
j=(""+i["date_died"]).split('-')
const date1=new Date('1/1/2020')
if(i["date_died"]=="9999-99-99"){
    dates=0
}
else{
    dates=1
}

//console.log(i["sex"])
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
parseInt(i["pregnancy"]),
parseInt(i["renal_chronic"]),
parseInt(i["tobacco"])
]
ActualArray.push(ActualElement)
}
function euclidean(a,b){
dist=0
    for(let i =0;i<a.length;i++){
        dist=dist+((a[i]-b[i])*(a[i]-b[i]))
}
dist=Math.sqrt(dist)
return dist
}


function printer(testArr){
    tempData=testArr
    mini=99999999
    exii=''
    miniArray=[]
exiiArray=[]
for(let j=0;j<Math.sqrt(ActualArray.length);j++){
miniArray.push(99999999)
exiiArray.push(-1)
}
    for(let jj=0;jj<ActualArray.length;jj++)
    {
        gg=euclidean(ActualArray[jj],tempData)
      /*  if(gg<mini){
            mini=gg
            exii=ActualArray[jj]
        */    
       for(let kk=0;kk<miniArray.length;kk++){
        if(gg<=miniArray[kk]){
            miniArray[kk]=gg
            exiiArray[kk]=ActualArray[jj]
            break;
        }
    }
        }
        sumi=0
        count=0
        for(let hi=0;hi<exiiArray.length;hi++){
            if(exiiArray[hi]!=-1){
            if(exiiArray[hi][5]!=3){
                sumi=sumi+exiiArray[hi][5]
            }
            else{
                sumi=sumi+0
            }
        count++
        }
        }
        res=(sumi/count)*33;
        document.getElementById("result").innerHTML=Math.ceil(res*100)/100+"%";
        //console.log(exiiArray)
    }

function FeatureEngineering(dataframe){
indexList=[1,7,8,9,6,10,11,12,14,15,16,17,18,19,21,22,5]
for(let j=1;j<560000;j++){
    element={}
    for(let i=0;i<this.indexList.length;i++){
        element[dataframe[0][this.indexList[i]]]=dataframe[j][this.indexList[i]];
    }    
finalJSON[0].push(element)
LabelEncoding(finalJSON[0][j-1])

}
//console.log(finalJSON)
//printer()
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