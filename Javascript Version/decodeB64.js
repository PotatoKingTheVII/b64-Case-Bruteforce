//From https://stackoverflow.com/a/28033962
var perm = function(str)
{
	var results = [];
	var arr = str.split("");
	var len = Math.pow(arr.length, 2);

	for( var i = 0; i < len; i++ )
	{
	  for( var k= 0, j = i; k < arr.length; k++, j >>=1)
	  {
		arr[k] = ( j & 1 ) ? arr[k].toUpperCase() : arr[k].toLowerCase();
	  }
	  var combo = arr.join("");
	  results.push(combo);
	}
	return results;
}


//Return true if the b64 decoded only contains ascii from range 32 to 126
function isValidb64(b64)
{
	try
	{
		decoded = atob(b64);
	}
	catch
	{
		return false //Most likely was something like x===, not carrying enough bits
	}

	for (let i = 0; i < decoded.length; i++)
	{
		if(decoded.charCodeAt(i) < 32 || decoded.charCodeAt(i) > 126)
		{
			return false
		}
	}

	return true
}

//Gather all the selected list options together for the plaintext to be shown
function updateOutput()
{
	var finalGuess = "";
	select_boxes = document.getElementsByTagName("select");
	for (let i = 0; i < select_boxes.length; i++)
	{
		var current_chunk = select_boxes[i].value;
		if(current_chunk == "")
		{
			finalGuess += "###";
		}
		else
		{
			finalGuess+=select_boxes[i].value;
		}
	}
	document.getElementById('outputTxt').value = finalGuess;
}



function bruteforce(ciphertext) 
{
	var b64length = ciphertext.length;
	
	//Create list of all chunks of 4 from ciphertext
	var chunkList = [];
	
	for (let i = 0; i < b64length; i+=4)
	{
		chunkList.push(ciphertext.slice(i, i+4));
	}

	//Loop through each chunks combinations checking for all valid cases
	var possibleB64 = [];
	for( var i = 0; i < chunkList.length; i++ )
	{
		var chunkPossibilities = [];
		var comboList = [...new Set(perm(chunkList[i]))];	//Make list of all case combos and only keep unique ones

		
		//For each of the unqique combinations found add any valid ones that give printable ascii
		for( var j = 0; j < comboList.length; j++ )
		{
			current_combo = comboList[j];
			if(isValidb64(current_combo))
			{
				chunkPossibilities.push(atob(current_combo));
			}
			
		}
		possibleB64.push(chunkPossibilities);
		
	}
	
	//At this point possibleB64 contains all the possible printable chunks for the ct
	//Combine all lower guesses for the final output
	var finalGuess = "";
	for( var i = 0; i < possibleB64.length; i++ )
	{
		try
		{
			var current_chunk = possibleB64[i][0];
			if(current_chunk == undefined)
			{
				finalGuess += "###";
			}
			else
			{
				finalGuess+=possibleB64[i][0];
			}					
		}
		
		catch
		{
			finalGuess += "###";
		}
	}
	
	//Set the output to this final guess
	document.getElementById('outputTxt').value = finalGuess;
	
	//Add select lists for each 4 chunk possability so
	//The user can manually change it themselves
	//First check if any exist already, if so then remove all of them so we don't keep adding
	if(document.getElementsByTagName("select").length != 0)
	{
		select_boxes = document.getElementsByTagName("select")
		
		//Dirty workaround because it kept missing elements
		while(true)
		{
			try
			{
				select_boxes[0].remove();
			}
			catch
			{
				break
			}
		}		
	}
	
	//Now make new select boxes and populate their options with our choices
	//https://stackoverflow.com/a/17002049
	var myParent = document.getElementById("selectBoxes");
	for( var i = 0; i < possibleB64.length; i++ )
	{

		//Create array of options to be added
		var array = possibleB64[i];

		//Create and append select list
		var selectList = document.createElement("select");
		selectList.id = "mySelect"+i;
		selectList.size = "2";
		selectList.onchange = updateOutput;

		myParent.appendChild(selectList);

		//Create and append the options
		for (var j = 0; j < array.length; j++) 
		{
			var option = document.createElement("option");
			option.value = array[j];
			option.text = array[j];
			selectList.appendChild(option);
			selectList.selectedIndex = 0;
		}
	}
	
}
