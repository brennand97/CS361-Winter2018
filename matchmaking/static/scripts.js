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
		var query = baseurl + zipcode + '/';
		var payload = generatePayload(); 

		if (zipcode != "")
		{
			
			//TODO: need some logic here to find if we are just searching on zipcode or filtering by preferences.

			//req.open('GET', query); //GET req if searching by zipcode
			req.open('POST', query); //POST req if filtering by preferences

			//csrf token needed for POST requests, maybe GET as well?  Leave for both.
			var csrftoken = getCookie('csrftoken');
			req.setRequestHeader('X-CSRFToken', csrftoken);
			req.setRequestHeader("Content-type","application/x-www-form-urlencoded");

			req.addEventListener('load',function(){
				if(req.status >= 200 && req.status < 400){
					//DOM Manipulation here.
					response = JSON.parse(req.responseText);
					results = document.getElementById('results');
					addDogsToDOM(response);
				}
				else{
					console.log("Error in network request: " + req.statusText);
				}
			});
		
			req.send(JSON.stringify(payload)); //TODO: send the JSON payload here
		
		}
		else
		{
			alert("You need to at least enter a zipcode to search for dogs.")
		}

		event.preventDefault();
	})
}

function getRadioValue(name) {
	var radios = document.getElementsByName(name);

	for (var i = 0, length = radios.length; i < length; i++)
	{
		if (radios[i].checked)
		{
			return radios[i].value;
		}
	}

	return null;
}

function convertOptToValue(value) {
	switch(value) {
		case 1:
			return null;
		case 2:
			return true;
		case 3:
			return false;
		default:
			return null;
	}
}

function weightMinMax(value) {
	switch(value) {
		case "any":
			return {
				min: null,
				max: null
			};
		case "small":
			return {
				min: null,
				max: 25
			};
		case "medium":
			return {
				min: 25,
				max: 50
			};
		case "large":
			return {
				min: 50,
				max: null
			};
		default:
			return {
				min: null,
				max: null
			};
	}
}

function heightMinMax(value) {
	switch(value) {
		case "any":
			return {
				min: null,
				max: null
			};
		case "short":
			return {
				min: null,
				max: 24
			};
		case "average":
			return {
				min: 24,
				max: 36
			};
		case "tall":
			return {
				min: 36,
				max: null
			};
		default:
			return {
				min: null,
				max: null
			};
	}
}

//Creates a payload from the html input fields
function generatePayload() {
	
	sex = getRadioValue("sex");
	sex = sex === "either" ? null : sex;
	color = document.getElementById("color").value.toLowerCase();
	color = color === "" ? null : color;
	height = heightMinMax(
		document.getElementById("height-opt").value
	);
	weight = weightMinMax(
		document.getElementById("weight-opt").value
	);
	eye_color = document.getElementById("eye-color-opt").value.toLowerCase();
	eye_color = eye_color === "any" ? null : eye_color;
	hypo = convertOptToValue(
		document.getElementById("hypoallergenic-opt").value
	);
	shedding = convertOptToValue(
		document.getElementById("shedding-opt").value
	);
	friendly = convertOptToValue(
		document.getElementById("friendly-opt").value
	);
	kid_friendly = convertOptToValue(
		document.getElementById("kid-friendly-opt").value
	);
	likes_water =convertOptToValue(
		document.getElementById("likes-water-opt").value
	);
	likes_cars = convertOptToValue(
		document.getElementById("likes-cars-opt").value
	);
	socialized = convertOptToValue(
		document.getElementById("socialized-opt").value
	);
	rescue_animal = convertOptToValue(
		document.getElementById("resuce-animal-opt").value
	);
	
	payload = {
		dog: {
			sex: sex,
			min_age: null,
			max_age: null,
			breed: null
		},
		physical: {
			color: color,
			min_height: height.min,
			max_height: height.max,
			min_weight: weight.min,
			max_weight: weight.max,
			eye_color: eye_color,
			hypoallergenic: hypo,
			shedding: shedding
		},
		personality: {
			friendly: friendly,
			kid_friendly: kid_friendly,
			likes_water: likes_water,
			likes_cars: likes_cars,
			socialized: socialized,
			rescue_animal: rescue_animal
		}
	};

	return payload;
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