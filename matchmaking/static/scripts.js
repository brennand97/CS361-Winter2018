document.addEventListener('DOMContentLoaded', bindSubmit);

// This allows us to get the csrf token, so we can do POST queries.  Taken from Django Website.
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

//binds an event to the submit button on the search page.  
function bindSubmit(){
	document.getElementById('submit').addEventListener('click',function(event){
		var req = new XMLHttpRequest();
		var zipcode = document.getElementById('zipcode').value;
		var baseurl = 'http://localhost:8000/search/';
		var query = baseurl + zipcode + '/'
		var payload = {}; 

		if (zipcode != "") {
			
			//TODO: need some logic here to find if we are just searching on zipcode or filtering by preferences.

			req.open('GET', query); //GET req if searching by zipcode
			//req.open('POST', query); //POST req if filtering by preferences

			//csrf token needed for POST requests, maybe GET as well?  Leave for both.
			var csrftoken = getCookie('csrftoken');
			req.setRequestHeader('X-CSRFToken', csrftoken);
			req.setRequestHeader("Content-type","application/x-www-form-urlencoded");

			req.addEventListener('load',function(){
				if(req.status >= 200 && req.status < 400){
					//DOM Manipulation here.
					response = JSON.parse(req.responseText);
					results = document.getElementById('results')
					addDogsToDOM(response)
				}
				else{
					console.log("Error in network request: " + req.statusText)
				}
		})
		
		req.send(null) //TODO: send the JSON payload here
		event.preventDefault();
		}
	})
}

function addDogsToDOM(response){
	//delete any previous results
	while (results.firstChild){
		results.removeChild(results.firstChild)
	}

	//loop through dogs
	for (i=0; i < response.length; i++){
		//create all HTML elements needed for each dog
		var container = document.createElement('div')
		container.className = "dogContainer"
		var dog = document.createElement("div")
		var name = document.createElement("h5")
		var a = document.createElement("a")
		var sex = document.createElement('p')
		var age = document.createElement('p')
		var breed = document.createElement('p')
		var bio = document.createElement('p')

		//add text content to elements
		a.textContent = response[i].name;
		a.href = '#'
		sex.textContent = "Sex: " + response[i].sex
		age.textContent = "Age: " + response[i].age
		breed.textContent = "Breed: " + response[i].breed
		bio.textContent = "Bio: " + response[i].bio

		//append elements to DOM
		name.appendChild(a)
		container.appendChild(name)
		container.appendChild(sex)
		container.appendChild(age)
		container.appendChild(breed)
		container.appendChild(bio)
		results.appendChild(container)
	} 
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