var request = require('request');
// Retrieve



api_key = 'AIzaSyBB9KLa1_lrVbPGagttplCeVtoWZ5f0d0o'
var request_tally = 0;
var has_hours = 0;


function request_details(place_id) {
  var request_url = 'https://maps.googleapis.com/maps/api/place/details/json?placeid='+place_id+'&key=' + api_key
  request(request_url, function (error, response, body) {
    if (!error && response.statusCode == 200) {
      var obj = JSON.parse(body)
      //console.log(obj.result.opening_hours.periods)
      console.log(obj)
    }
    else {
      console.log(body)
      console.log(error)
    }
  })
}
function find_places(request_url) {
  console.log(request_url);
  request(request_url,
      function (error, response, body) {
        if (!error && response.statusCode == 200) {
          var obj = JSON.parse(body);
          console.log(obj.status)
          if (obj.next_page_token) {
            console.log("got one: "+obj.next_page_token);
            console.log('https://maps.googleapis.com/maps/api/place/nearbysearch/json?pagetoken='+obj.next_page_token+'&key=' + api_key);
            setTimeout(function() {
              find_places('https://maps.googleapis.com/maps/api/place/nearbysearch/json?pagetoken='+obj.next_page_token+'&key=' + api_key);
            }, 10000);

          } else {
            console.log("didn't");
            console.log(obj);
          }
          obj.results.filter(function (result) {
            if (result.opening_hours) return result
          }).map(function (result) {
            has_hours += 1;
            request_details(result.place_id);
          }); // Print the google web page.
        }
        else {
          console.log(body)
          console.log(error)
        }
        request_tally += obj.results.length;
        console.log(request_tally);
        console.log("has Hours: " + has_hours)
      })
}

var main = function(){
  find_places('https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=48.4222,-123.3657&radius=100&key=' + api_key)


};

if (require.main === module) {
  main();
}


