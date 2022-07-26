const req_url = "http://128.119.246.170:7789/extract";


// selecting loading div
const loader = document.getElementById("loading");
const textarea = document.getElementById("textarea");
const error = document.getElementById("error");

// showing loading
function displayLoading() {
    loader.style.display = "flex"
    textarea.style.display = "none";
    error.style.display = "none";
    // to stop loading after some time
    //setTimeout(() => {
        //loader.style.display = "none";
    //}, 90000); //Maximum 1min30s
}

// hiding loading 
function hideLoading() {
    loader.style.display = "none";
    textarea.style.display = "block";
}

// hiding loading 
function hideLoadingError() {
    loader.style.display = "none";
    error.style.display  = "block";
}

function submitRequest(){
    var input = document.getElementById("search").value;
    callAPI(input);
}

function callAPI(input){
    let request = new XMLHttpRequest();
    request.open("POST", req_url);
    request.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    displayLoading();
    console.log("Submitting: " + input);
    try{
        request.send(JSON.stringify({ "query": input }));

        request.onerror = () => {
            hideLoadingError();
            console.log(`error ${request.status}: ${request.statusText}`)
        }

        request.onload = () => {
            console.log(request);
            if (request.status == 200) {
                var resJson = JSON.parse(request.response);
                hideLoading();
                constructDynamicContent(resJson);
            }
            else {
                hideLoadingError();
                console.log(`error ${request.status}: ${request.statusText}`)
            }
        }
    }catch(e){
        hideLoadingError();
        console.log('catch', e);
  }
}

//Copy Content
document.getElementById("copyBtn").onclick = function(){
    var content = document.getElementById("text");
    copyToClipboard(content);
}

function copyToClipboard(element) {
    var $temp = $("<input>");
    $("body").append($temp);
    $temp.val($(element).text()).select();
    document.execCommand("copy");
    $temp.remove();
}

function constructDynamicContent(resJson){
    var baseurl = "https://www.google.com/search?q=";
    document.getElementById("clariq").innerHTML = resJson['clariQ'][0];
    document.getElementById("text").innerHTML = "<b>Fascets:</b> \n" + resJson['fascets'] +
                                                "\n <b>Best Fascets:</b> \n" + resJson['bestFascets'] +
                                                "\n <b>Question:</b> \n"+ resJson['clariQ'][0];

    var fascets = resJson['bestFascets'].split(' , ');
    var innerHTML = "";

    if(fascets[0] == ""){

        var googleurl = baseurl + resJson['query'];
        innerHTML = '<a href="' + googleurl + '" class="w3-bar-item w3-button" target="_blank">' + resJson['query'] + '</a>'
        document.getElementById("bestFascets").innerHTML = innerHTML;
        document.getElementById("bestFascets-full").innerHTML = innerHTML;
    }
    else{

        for (var i = 0; i < fascets.length; i++){
            var googleurl = baseurl + resJson['query'] + "+" + fascets[i].replace(" ", "+");
            innerHTML = innerHTML + '<a href="' + googleurl + '" class="w3-bar-item w3-button" target="_blank">' + fascets[i] + '</a>';
            if(i>=5){
                break;
            }
        }
        document.getElementById("bestFascets").innerHTML = innerHTML;
        
        var innerHTML = "";
        for (var i = 0; i < fascets.length; i++){
            var googleurl = baseurl + resJson['query'] + "+" + fascets[i].replace(" ", "+");
            innerHTML = innerHTML + '<a href="' + googleurl + '" class="w3-bar-item w3-button" target="_blank">' + fascets[i] + '</a>';
        }
        document.getElementById("bestFascets-full").innerHTML = innerHTML;
    }

    
}


var coll = document.getElementsByClassName("collapsible");
var i;

for (i = 0; i < coll.length; i++) {
  coll[i].addEventListener("click", function() {
    this.classList.toggle("active");
    document.getElementById("content").classList.toggle("content_active");
    document.getElementById("col_icon").classList.toggle("collapse_icon_active");
    document.getElementById("col_icon").classList.toggle("fa-flip-horizontal");
    document.getElementById("btn_text").classList.toggle("hideContent");
    document.getElementById("btn_text").classList.toggle("showContent");
    
    var content = this.nextElementSibling;
    if (content.style.maxHeight){
      content.style.maxHeight = null;
    } else {
      content.style.maxHeight = (content.scrollHeight + 50) + "px";
    } 
  });
}

