//This file is for client-side searching

var savedContents;

window.onload = function() {
	var searchTerm = document.getElementsByClassName("search")[0].value = "";
}

function search(event) {
	//console.log(event.key);
	var searchTerm = document.getElementsByClassName("search")[0].value;
	//console.log(searchTerm);
	var results = searchResults(searchTerm);
	var holder;
	if (document.getElementsByClassName("normal-body-header-container").length === 0) {
		//document is a navigation page
		holder = document.getElementsByClassName("body-header-container")[0];
	} else {
		//document is normal text page
		holder = document.getElementsByClassName("normal-body-header-container")[0];
	}
	if (savedContents === undefined) {
		savedContents = holder.innerHTML;
	}
	if (searchTerm === "") {
		console.log("search term removed, reverting page");
		holder.innerHTML = savedContents;
	} else {
		holder.innerHTML = "";
		holder.innerHTML += "<h2 class=\"bodyheader\">Search Results</h2>";
		for (var i = 0; i < Math.min(results.length, 10); i++) {
			holder.innerHTML += "<a href="+pageDescriptions[results[i][0]][1]+"><p>"+pageDescriptions[results[i][0]][0]+"</p></a>"
		}
	}
}

var pageDescriptions = [[pageDescriptions]];
var searchTerms = [[searchTerms]];


function searchResults(term) {
	term = term.toLocaleLowerCase().split(" ");
	var res = [];
	//[address, index]
	for (var i = 0; i < term.length; i++) {
		for (var j = 0; j < searchTerms.length; j++) {
			//console.log("Comparing "+term[i]+" and "+searchTerms[j][0]);
			var n = searchIndex(term[i], searchTerms[j][0]) / pageDescriptions[searchTerms[j][1]][2];
			//console.log("\tThey got a score of: "+n);
			if (n > 0) {
				var found = false;
				for (var k = 0; k < res.length; k++) {
					if (res[k][0] === searchTerms[j][1]) {
						found = true;
						//console.log("\t\texisting entry exists, adding");
						res[k][1]+=n;
						break;
					}
				}
				if (!found) {
					//console.log("\t\texisting entry not found, adding entry");
					res.push([searchTerms[j][1], n]);
				}
			}
		}
	}
	function compare(a, b) {
		if (a[1] < b[1]) {
			return -1;
		}
		if (a[1] > b[1]) {
			return 1;
		}
		return 0;
	}
	return res.sort(compare).reverse();
}

function searchIndex(a, b) {
	var small, large;
	if (a.length > b.length) {
		large = a;
		small = b;
	} else {
		large = b;
		small = a;
	}

	var testN = small.length + large.length - 1;
	var maxMatch = 0;
	for (var i = 0; i < testN; i++) {
		var minI = Math.max(0, i - small.length + 1);
		var maxI = Math.min(large.length, i+1);
		var matches = 0;
		for (var j = minI; j < maxI; j++) {
			//console.log("\t\tcomparing " + small[j-i+small.length-1] + " and " + large[j]);
			if (small[j-i+small.length-1] === large[j]) {
				matches++;
			}
		}
		//console.log("found "+matches+" matches");
		maxMatch = Math.max(maxMatch, matches);
	}
	//console.log("Max matches: "+maxMatch);
	//console.log("result: "+maxMatch / small.length)
	if (large.length === 0) {
		return 0;
	}
	return maxMatch / large.length;
}

function printRecipe() {
	console.log("printing");
	var wholePage = document.body.innerHTML;
	var holder;
	if (document.getElementsByClassName("normal-body-header-container").length === 0) {
		//document is a navigation page
		holder = document.getElementsByClassName("body-header-container")[0];
	} else {
		//document is normal text page
		holder = document.getElementsByClassName("normal-body-header-container")[0];
	}

	document.body.innerHTML = holder.innerHTML;
	document.body.removeChild(document.body.firstElementChild)

	window.print();

	document.body.innerHTML = wholePage;
}