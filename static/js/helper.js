var $ = (id) => document.getElementById(id);
var println = (s) => console.log(s);

function waiveWec(){
  
  let wecCheck = $("wec_event");
  let admitOne = $("admit_one");

  if (wecCheck.checked) {
    admitOne.value = "WAIVED" 
  } else {
    admitOne.value = ""
  }
}

function validateTime(){

  let startMin = inputToMin($('starts').value);
  let endMin = inputToMin($('ends').value);

  if(isNaN(startMin) || isNaN(endMin)){
    $('error').innerHTML = 'invalid start or end time.';
    $('submit').disabled = true;
    return false;
  }

  // end needs to be after start 
  if(endMin < startMin) {
    $('error').innerHTML = 'start time is after end time';
    $('submit').disabled = true;
    return false;
  }

  let quantity = Math.ceil((endMin - startMin) / (4 * 60));

  $('error').innerHTML = '';
  $('status').innerHTML = `total will be $ ${quantity}0 (quantity of ${quantity})`;

  return true;
}

function validateAdMitOne(){
  let regex = /^[A-Z]{6}$/;
  let check = $('admit_one').value;

  if(!regex.test(check)){ 
    $('error').innerHTML = 'invalid adMitOne code. (must be six alphabets, eg: \'ABCDEF\')';
    $('submit').disabled = true;
    return false;
  }

  return true
}

function validate(){
  if (validateTime() && validateAdMitOne()){
    $('error').innerHTML = '';     
    $('submit').disabled = false;
  }
}

function inputToMin(time){

  let t= time.split(':');
  let hour = +t[0];
  let minute = +t[1];

  return hour * 60 + minute;
}
