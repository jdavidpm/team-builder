document.getElementById("interestsFilterButton").onclick = addInterest;
document.getElementById("experiencesFilterButton").onclick = addExperience;
document.getElementById("fieldsFilterButton").onclick = addField;

function addInterest()
{
	interest = document.getElementById("interestsFilter").value;

	if (!document.getElementById("spn_"+interest))
	{
		spanInterest = document.createElement("span");
		spanInterest.setAttribute("class", "badge badge-pill badge-secondary d-flex align-items-center pl-3");
		spanInterest.setAttribute("id", "spn_"+interest);
		spanInterest.innerHTML = interest; 

		inputInterest = document.createElement("input");
		inputInterest.setAttribute("type","hidden");
		inputInterest.setAttribute("name","interest_"+interest);
		inputInterest.setAttribute("value",interest);


		buttonInterest = document.createElement("button");
		buttonInterest.setAttribute("type", "button");
		buttonInterest.setAttribute("class", "close ml-2 mb-1 text-danger");
		buttonInterest.setAttribute("id", "btn_"+interest);
		buttonInterest.setAttribute("aria-label", "Close");
		
		hidInterest = document.createElement("span");
		//hidInterest.setAttribute("aria-hidden", "true");
		hidInterest.setAttribute("id", "hid_"+interest);
		hidInterest.innerHTML = "&times;";

		buttonInterest.appendChild(hidInterest);
		spanInterest.appendChild(buttonInterest);
		spanInterest.appendChild(inputInterest);
		document.getElementById("badgesDiv").appendChild(spanInterest);

		document.getElementById("badgesDiv").addEventListener('click', function(event) {
			funRemove(event.target);
			});
	}

}
function funRemove(element)
{
	element.parentNode.parentNode.parentNode.removeChild(element.parentNode.parentNode);
	
}
function addExperience()
{
	experience = document.getElementById("experiencesFilter").value;

	if (!document.getElementById("spn_"+experience))
	{
		spanInterest = document.createElement("span");
		spanInterest.setAttribute("class", "badge badge-pill badge-secondary d-flex align-items-center pl-3");
		spanInterest.setAttribute("id", "spn_"+experience);
		spanInterest.innerHTML = experience; 

		inputInterest = document.createElement("input");
		inputInterest.setAttribute("type","hidden");
		inputInterest.setAttribute("name","experience_"+experience);
		inputInterest.setAttribute("value",experience);


		buttonInterest = document.createElement("button");
		buttonInterest.setAttribute("type", "button");
		buttonInterest.setAttribute("class", "close ml-2 mb-1 text-danger");
		buttonInterest.setAttribute("id", "btn_"+experience);
		buttonInterest.setAttribute("aria-label", "Close");
		
		hidInterest = document.createElement("span");
		//hidInterest.setAttribute("aria-hidden", "true");
		hidInterest.setAttribute("id", "hid_"+experience);
		hidInterest.innerHTML = "&times;";

		buttonInterest.appendChild(hidInterest);
		spanInterest.appendChild(buttonInterest);
		spanInterest.appendChild(inputInterest);
		document.getElementById("badgesDiv").appendChild(spanInterest);

		document.getElementById("badgesDiv").addEventListener('click', function(event) {
			funRemove(event.target);
			});
	}

}
function addField()
{
	field = document.getElementById("fieldsFilter").value;

	if (!document.getElementById("spn_"+field))
	{
		spanInterest = document.createElement("span");
		spanInterest.setAttribute("class", "badge badge-pill badge-secondary d-flex align-items-center pl-3");
		spanInterest.setAttribute("id", "spn_"+field);
		spanInterest.innerHTML = field; 

		inputInterest = document.createElement("input");
		inputInterest.setAttribute("type","hidden");
		inputInterest.setAttribute("name","field_"+field);
		inputInterest.setAttribute("value",field);


		buttonInterest = document.createElement("button");
		buttonInterest.setAttribute("type", "button");
		buttonInterest.setAttribute("class", "close ml-2 mb-1 text-danger");
		buttonInterest.setAttribute("id", "btn_"+field);
		buttonInterest.setAttribute("aria-label", "Close");
		
		hidInterest = document.createElement("span");
		//hidInterest.setAttribute("aria-hidden", "true");
		hidInterest.setAttribute("id", "hid_"+field);
		hidInterest.innerHTML = "&times;";

		buttonInterest.appendChild(hidInterest);
		spanInterest.appendChild(buttonInterest);
		spanInterest.appendChild(inputInterest);
		document.getElementById("badgesDiv").appendChild(spanInterest);

		document.getElementById("badgesDiv").addEventListener('click', function(event) {
			funRemove(event.target);
			});
	}

}