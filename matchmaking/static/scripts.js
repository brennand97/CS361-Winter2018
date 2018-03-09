document.addEventListener('DOMContentLoaded', bindSubmit);

// This allows us to get the csrf token, so we can do POST queries.
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

//get the token
var csrftoken = getCookie('csrftoken');

//binds an event to the submit button on the search page.  
function bindSubmit(){
	document.getElementById('submit').addEventListener('click',function(event){
		var req = new XMLHttpRequest();
		var zipcode = document.getElementById('zipcode').value;
		var baseurl = 'http://localhost:8000/search/';
		var query = baseurl + zipcode + '/'
		
		if (zipcode != "") {
		req.open('GET', query);
		req.setRequestHeader('X-CSRFToken', csrftoken);
		req.setRequestHeader("Content-type","application/x-www-form-urlencoded");

		req.addEventListener('load',function(){
			if(req.status >= 200 && req.status < 400){
				//DOM Manipulation here.
				response = JSON.parse(req.responseText);
				results = document.getElementById('results')

				//delete any previous results
				while (results.firstChild){
					results.removeChild(results.firstChild)
				}

				for (i=0; i < response.length; i++){
					var container = document.createElement('div')
					container.className = "dogContainer"
					var dog = document.createElement("div")
					var name = document.createElement("h5")
					var a = document.createElement("a")
					var sex = document.createElement('p')
					var age = document.createElement('p')
					var breed = document.createElement('p')
					var bio = document.createElement('p')

					a.textContent = response[i].name;
					a.href = '#'
					sex.textContent = "Sex: " + response[i].sex
					age.textContent = "Age: " + response[i].age
					breed.textContent = "Breed: " + response[i].breed
					bio.textContent = "Bio: " + response[i].bio

					name.appendChild(a)
					container.appendChild(name)
					container.appendChild(sex)
					container.appendChild(age)
					container.appendChild(breed)
					container.appendChild(bio)
					results.appendChild(container)
				} 
			}
			else{
				console.log("Error in network request: " + req.statusText)
			}
		})
		
		req.send(null)
		event.preventDefault();
		}
	})
}

function listView() {
	var containers = document.getElementsByClassName("dogContainer");
	for (var i=0; i < containers.length; i++) {
		containers[i].style.width = "100%"; 
	}
}

function tileView() {
	var containers = document.getElementsByClassName("dogContainer");
	console.log(containers.length);
	for (var i=0; i < containers.length; i++) {
		containers[i].style.width = "50%"; 
	}
}