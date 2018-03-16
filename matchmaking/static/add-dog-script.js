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

//binds an event to the submit button on the search page.  
function bindSubmit(){
	document.getElementById('submit').addEventListener('click',function(event){
		event.preventDefault();
		var req = new XMLHttpRequest();
		var baseurl = 'http://localhost:8000/add_dog_to_db/';
		var payload = generatePayload();
		payload.user = document.getElementById("user").value

		console.log(payload)

		//don't do POST request unless there's at least a name and zipcode.  Pretty worthless otherwise.
		if (payload.dog['name'] === null || payload.dog['zipcode'] === null) {
			window.alert("Enter at least a name and zipcode to add dog.")
		}
		else{
			
			req.open('POST', baseurl);
			//get the token
			var csrftoken = getCookie('csrftoken');
			req.setRequestHeader('X-CSRFToken', csrftoken);
			req.setRequestHeader("Content-type","application/json");

			req.addEventListener('load',function(){
				if(req.status >= 200 && req.status < 400){
						//success message
						window.alert(payload.dog['name'] + " added successfully!");
				}
				else{
					window.alert("Oops, something went wrong.  Please try again.");
					console.log("Error in network request: " + req.statusText);
				}
			})
			req.send(JSON.stringify(payload))
		}
	})
}

//Creates an empty payload object.
function generateEmptyPayload(){
	var payload = {
		"user": null,
  		"dog": {
  			"name": null,
    		"sex": null,
    		"age": null,
    		"breed": null,
    		"city": null,
    		"state": null,
    		"zipcode": null,
    		"bio": null
  		},
  		"physical": {
    		"color": null,
    		"height": null,
    		"weight": null,
    		"eye_color": null,
    		"hypoallergenic": false,
    		"shedding": false
  		},
  		"personality": {
    		"friendly": false,
    		"kid_friendly": false,
    		"likes_water": false,
    		"likes_cars": false,
    		"socialized": false,
   			"rescue_animal": false
  		}
	}
	return payload;
}

//Some jQuery to get all of the form data quicky.
function getFormData(){
    form = document.getElementById("add-dog-form")
    var array = jQuery(form).serializeArray();
    var json = {};
    
    jQuery.each(array, function() {
        json[this.name] = this.value || '';
    }); 

    return json;
}

//Fills an empty payload object with form data
function generatePayload(){
	payload = generateEmptyPayload();
	formData = getFormData();

	//here we grab every property in form data and assign it's corresponding value to payload
	for (var prop in formData){
		if (!formData.hasOwnProperty(prop)) continue;
		
		if(formData[prop] === ""){
			formData[prop] = null;
			continue;
		}

		if (prop == 'city' || prop == 'state' || prop == 'name' || prop == 'sex' || prop == 'breed' || prop == 'age' || prop == 'zipcode' || prop == 'bio'){
			payload.dog[prop] = formData[prop]
		}

		else if (prop == 'color' || prop == 'height' || prop == 'weight' || prop == 'hypoallergenic' || prop == 'shedding'){
			payload.physical[prop] = formData[prop]
		}

		else {
			if (prop != 'csrfmiddlewaretoken'){ //we dont want to include this in payload
				payload.personality[prop] = formData[prop]
			}
		}	
	}

	//eye color has to be handled seperately because it is a dropdown.
	var e = document.getElementById("eye_color");
	if(e.value != "any"){ //any is no preference. We will just leave eye color as null in this case
		payload.physical["eye_color"] = e.value
	}

	//some of the items in formData got converted to strings.  This converts back to ints.
	payload = fixPayload(payload)

	return payload
}

//some of the payload's data was converted integers to strings.  This fixes that.
function fixPayload(payload){
	keys = ['zipcode', 'age', 'height', 'weight']
	for(var i = 0; i < keys.length ; i++){
			if (keys[i] == 'zipcode' || keys[i] == 'age'){
				if (payload.dog[keys[i]] != null) { //can't run parseInt() on null
					payload.dog[keys[i]] = parseInt(payload.dog[keys[i]])
				}
			}
			if (keys[i] == 'weight' || keys[i] == 'height'){
				if (payload.physical[keys[i]] != null) {//can't run parseInt() on null
					payload.physical[keys[i]] = parseInt(payload.physical[keys[i]])
				}
			}
	}
	return payload
}


