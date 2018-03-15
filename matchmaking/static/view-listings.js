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

// Get the token
var csrftoken = getCookie('csrftoken');

// Binds an event to the submit button on the view_listings page.  
function bindSubmit(){
	document.getElementById('submitListing').addEventListener('click',function(event){
		event.preventDefault();
		var req = new XMLHttpRequest();
		var baseurl = 'http://localhost:8000/shelter_dogs/';
		var shelter = document.getElementById('shelterName').value;
		var query = baseurl + shelter + '/';


		if (shelter == "") {
			window.alert("Please enter the shelter account name.");
		}
		
		if (shelter != "") {
		req.open('GET', query);
		req.setRequestHeader('X-CSRFToken', csrftoken);
		req.setRequestHeader("Content-type","application/json");

		req.addEventListener('load',function(){
			if(req.status >= 200 && req.status < 400){
				//DOM Manipulation here.
				response = JSON.parse(req.responseText);
				results = document.getElementById('listingResults');

				//delete any previous results
				while (results.firstChild){
					results.removeChild(results.firstChild);
				}

				for (i=0; i < response.length; i++) {
					var container = document.createElement('div');
					container.className = "dogContainer";
					container.id = response[i].name;
					var dog = document.createElement("div");
					var name = document.createElement("h5");
					var a = document.createElement("a");
					var sex = document.createElement('p');
					var age = document.createElement('p');
					var breed = document.createElement('p');
					var bio = document.createElement('p');
					var viewBtn = document.createElement('button');
					var editBtn = document.createElement('button');
					var deleteBtn = document.createElement('button');
					
					a.textContent = response[i].name;
					a.href = '#';
					sex.textContent = "Sex: " + response[i].sex;
					age.textContent = "Age: " + response[i].age;
					breed.textContent = "Breed: " + response[i].breed;
					bio.textContent = "Bio: " + response[i].bio;
					
					// Building view/edit/delete buttons
					viewBtn.textContent = "View";
					editBtn.textContent = "Edit";
					deleteBtn.textContent = "Delete";
					viewBtn.className = response[i].name;
					editBtn.className = response[i].name;
					deleteBtn.className = response[i].name;

					// View button opens dog page in new tab
					viewBtn.addEventListener("click", function() {
						var url = baseurl + this.className + '/';
						window.open(url, '_blank');
					})
					editBtn.addEventListener("click", function() {
						console.log("editBtn pressed.")
					})
					deleteBtn.addEventListener("click", function() {
						deleteFcn(this.className)
					})

					name.appendChild(a);
					container.appendChild(name);
					container.appendChild(sex);
					container.appendChild(age);
					container.appendChild(breed);
					container.appendChild(bio);
					container.appendChild(viewBtn);
					container.appendChild(editBtn);
					container.appendChild(deleteBtn);
					results.appendChild(container);
				} 
			}
			else{
				console.log("Error in network request: " + req.statusText);
			}
		})
		
		req.send(null)
		event.preventDefault();
		}
	})
}

// Delete POST request 
function deleteFcn(dogName) {
	event.preventDefault();
	var req = new XMLHttpRequest();
	var query = 'http://localhost:8000/' + "del_dog/";
	req.open('POST', query, true);
	req.setRequestHeader('X-CSRFToken', csrftoken);
	req.setRequestHeader("Content-type","application/json");
	
	var payload = {"name": dogName};
	console.log(payload);
	req.send(JSON.stringify(payload));
	req.addEventListener('load', function(){
		if(req.status >= 200 && req.status < 400){
				// Remove container id matching dog name
				var element = document.getElementById(dogName);
    			element.parentNode.removeChild(element);

				//success message
				window.alert(payload.name + " successfully removed!");
		}
		else{
			window.alert("Oops, something went wrong.  Please try again.");
			console.log("Error in network request: " + req.statusText);
		}
	})
}