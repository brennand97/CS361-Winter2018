document.addEventListener('DOMContentLoaded', bindSubmit);

// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');


function bindSubmit(){
	document.getElementById('submit').addEventListener('click',function(event){
		var req = new XMLHttpRequest();
		var zipcode = document.getElementById('zipcode').value;
		var baseurl = 'http://localhost:8000/search/';
		var query = baseurl + zipcode + '/'
		console.log(query)

		req.setRequestHeader('X-CSRFToken', csrftoken);
		//req.setRequestHeader("Content-type","application/x-www-form-urlencoded");
		req.open('POST', query);

		req.addEventListener('load',function(){
			event.preventDefault()
			if(req.status >= 200 && req.status < 400){
				//DOM Manipulation here.
				console.log("good req status")
				console.log(JSON.parse(req.responseText));
			}
			else{
				console.log("Error in network request: " + req.statusText)
			}
		})
		
		req.send(null)
		event.preventDefault()

	})


}