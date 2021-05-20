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