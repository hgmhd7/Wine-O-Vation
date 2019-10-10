// Create a variable to point and capture the UFO sightings data in my data.js
// var tableData = data;


// Create a variable to point to the table body for use in my table population below
var tbody = d3.select("tbody")


// Loop through each UFO sighting and populate the table when the user first visits the page name and call the printName function
// tableData.forEach((sighting) => {



d3.csv("static/js/REDUCED_RECOMMENDATION_master_wine_table.csv", function (err, wineData) {
  if (err) throw err;

  console.log(wineData);
  // Create new table row
  var row = tbody.append("tr")


  wineData.forEach(function (wineData) {

    Object.entries(wineData).forEach(function (key, value) {

      // append stats to the table
      row.append("td").text(value);

    });

  });
  // Iterate through each key and value

});




// function filterAll(userInput){

//     // Create another variable to point to the complete data set
//     var filteredData = tableData;

//     // DEBUGGER TO SEE IF I'M PROPERLY CATCHING MY USER IMPUT VALUE FROOM TEH HTML INPUT BOXES
//     // console.log(userInput.value);


//     // Declare and set my values for use below when I load them into the filterList object
//     dateValue = d3.select("#datetime").property("value"); 
//     cityValue = d3.select("#city").property("value").toLowerCase().trim();
//     stateValue = d3.select("#state").property("value").toLowerCase().trim();
//     countryValue = d3.select("#country").property("value").toLowerCase().trim();
//     shapeValue = d3.select("#shape").property("value").toLowerCase().trim();


//     // Create the filterList object
//     var filterList = {datetime : dateValue, 
//                       city : cityValue, 
//                       state : stateValue,
//                       country : countryValue,
//                       shape : shapeValue};



//     // DEBUGGER TO MAKE SURE I AM REDUCING MY DICTIONARY TO ONLY VALID INPUT
//     //console.log(filterList);



//     // Iterate through each key and value in the filterList and delete any entry that has a empty value so I dont throw an error when I try to filter
//     Object.entries(filterList).forEach(([key, value]) => {

//         if (value === ""){
//           delete filterList[key]; 
//         }

//     }); 


//     // DEBUGGER TO MAKE SURE I AM REDUCING MY DICTIONARY TO ONLY VALID INPUT
//     //console.log(filterList);



//     // Iterate through each key and value to filter the UFO data
//     Object.entries(filterList).forEach(([key, value]) => {

//         filteredData =  filteredData.filter(sighting => sighting[key] === value);  

//     }); 

//     // Clear out previous input to make way for the new filtered data 
//     tbody.html("");


//     filteredData.forEach((sighting) => {

//         // Create new table row
//         var row = tbody.append("tr");
//           // Iterate through each key and value
//         Object.entries(sighting).forEach(([key, value]) => {

//           // append sightings information to the table
//           row.append("td").text(value);

//             });
//         });
// };



// function clearInputFields(){

//     // Clear all my input fields when I click the "Reset Table" button
//     document.getElementById('datetime').value = '';
//     document.getElementById('city').value = '';
//     document.getElementById('state').value = '';
//     document.getElementById('country').value = '';
//     document.getElementById('shape').value = '';
// };




// function resetTable(){

//     // Call my function to clear all input fields
//     clearInputFields()

//     // Clear out current date to make way for original ufo data below
//     tbody.html("");

//     // Loop through each UFO sighting and populate the table when the user first visits the page
//     tableData.forEach((sighting) => {

//       // Create new table row
//       var row = tbody.append("tr")

//       // Iterate through each key and value
//       Object.entries(sighting).forEach(([key, value]) => {

//         // append sightings information to the table
//         row.append("td").text(value);
//       });
//     });
// };





















//*****************I'M KEEPING ALL THE BELOW CODE SHOWING DIFFERENT METHODS I TRIED TO SOLVE THIS PROBLEM...  MIGHT NEED THEM FOR FURTHER REFERENCE IN THE FUTURE... *************************//



// function filterAll(userInput){

//   // debugging to 
//   console.log(userInput.id);
//   console.log(userInput.value);


//   var filterList = [d3.select("#datetime").property("value"), d3.select("#city").property("value"), d3.select("#state").property("value")];

//   filterList = filterList.filter(filter => filter)

//   console.log(filterList);

//   if (userInput.value){


//   var filterSet = tableData.filter(sighting => sighting[userInput.id] === userInput.value);


//   tbody.html("");


//       filterSet.forEach((sighting) => {

//       var row = tbody.append("tr");
//         // Iterate through each key and value
//       Object.entries(sighting).forEach(([key, value]) => {

//         row.append("td").text(value);
//         // append stats to the list

//          });
//       });

//     }


//   }







    // filterSet.push(DateInputValue);


    // if (CityInputElement.property("value") !== undefined){

    //   var CityInputValue = CityInputElement.property("value");

    //   filterSet.push(CityInputValue);
    // };

    // if (StateInputElement.property("value") !== undefined){

    //   var StateInputValue = StateInputElement.property("value");

    //   filterSet.push(StateInputValue);
    // };



    // console.log(filterSet)

    // filterSet.forEach(function(sighting) {

    //   var allFilteredData = tableData.filter(sighting => sighting.info);
    // });

    // var allFilteredData = tableData.filter((sighting => filterSet.indexOf(sighting.datetime) !== -1) || (sighting => filterSet.indexOf(sighting.city) !== -1));


















  // function filterAll(){

  //   if (DateInputElement.property("value") === undefined){

  //     var DateInputValue = DateInputElement.val('empty');
  //   } else{
  //    // Get the value property of the input element
  //   var DateInputValue = DateInputElement.property("value");
  //   }


  //   if (CityInputElement.property("value") === undefined){

  //     var CityInputValue = CityInputElement.val('empty');
  //   } else{
  //       // Get the value property of the input element
  //     var CityInputValue = CityInputElement.property("value");
  //   }


  //   var allFilteredData = tableData.filter(sighting => sighting.datetime === DateInputValue && sighting.city === CityInputValue);


  //   tbody.html("");


  //   const tablfullfilter = allFilteredData.forEach((sighting) => {

  //     var row = tbody.append("tr");
  //       // Iterate through each key and value
  //     Object.entries(sighting).forEach(([key, value]) => {

  //       row.append("td").text(value);
  //       // append stats to the list

  //        });
  //     });
  // }


// if (DateInputElement.property("value") === Nothing){
//   // Loop through each student name and call the printName function
// tableData.forEach((sighting) => {

//   var row = tbody.append("tr")
//     // Iterate through each key and value
//     Object.entries(sighting).forEach(([key, value]) => {

//         row.append("td").text(value);
//         // append stats to the list

//      });
//   });
// };



  // CityInputElement.on("change", function(DateFiltered) {



  //   // Get the value property of the input element
  //   var inputValue = inputElement.property("value");

  //   var filteredData = DateFiltered.filter(sighting => sighting.city === inputValue);


  //   tbody.html("");


  //   const CityFiltered = filteredData.forEach((sighting) => {

  //     var row = tbody.append("tr")
  //       // Iterate through each key and value
  //       Object.entries(sighting).forEach(([key, value]) => {

  //           row.append("td").text(value);
  //           // append stats to the list

  //        });
  //     });


  //   return CityFiltered

  // });


// // Select the button
// var button = d3.select("#filter-btn");

// button.on("click", function() {

//   // Select the input element and get the raw HTML node
//   var inputElement = d3.select("#datetime");

//   // Get the value property of the input element
//   var inputValue = inputElement.property("value");

//   var filteredData = tableData.filter(tableData => tableData.datetime === inputValue);


// // BONUS: Calculate summary statistics for the age field of the filtered data

// // First, create an array with just the age values
// var city = filteredData.map(tableData => tableData.city);

// // // Next, use math.js to calculate the mean, median, mode, var, and std of the ages
// // var mean = math.mean(ages);
// // var median = math.median(ages);
// // var mode = math.mode(ages);
// // var variance = math.var(ages);
// // var standardDeviation = math.std(ages);

// // Then, select the unordered list element by class name
// var results_table = d3.select(".city");

// // remove any children from the list to
// results_table.html("");



// });
