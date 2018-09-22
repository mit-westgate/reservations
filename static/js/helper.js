function waiveWec(){
  
  let wecCheck = document.getElementById("wec_event");
  let admitOne = document.getElementById("admit_one");

  if (wecCheck.checked) {
    admitOne.value = "WAIVE" 
  } else {
    admitOne.value = ""
  }
}

function howmuch(){
  
  let start = document.getElementById("starts")

}

function hoursToMinutes(h, m, ap){
  let mins = 0;
  if(ap.toLowerCase() == 'pm'){
    mins += 60 * 12;  
  }

  
  
}
