 // JS function to check the value of input.

function validate() {	
	
	// Get the target node of the event
	var firstname = document.getElementById("firstname");
    var lastname = document.getElementById("lastname");
    var year = document.getElementById("year");

    var fn = firstname.value;
    var ln = lastname.value;
    var yr = year.value;

    console.log("fn  = "  + fn);
    console.log("ln  = "  + ln);
    console.log("yr  = "  + yr);

    // Check that all 3 input fields are not blank

    if ((fn == "" || fn.match(/^\s*$/)) &&
    	(ln == "" || ln.match(/^\s*$/)) && 
    	(yr == "" || yr.match(/^\s*$/))	) {
    	alert("Please provide a correct input! ");
    	return false;
    }

    else
    	return true;
}