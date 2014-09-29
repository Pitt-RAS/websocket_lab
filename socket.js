var point_queue = [];
var q_size = 0;

var connection = new WebSocket("ws://localhost:8765");
connection.onopen = function() {
  // modify some HTML element
  // to indicate that the socket is open
  alert("socket opened");
}

connection.onclose = function() {
  // modify another HTML DOM element
  alert("socket closed");
}

connection.onerror = function(error) {
  console.log("ERROR HAPPENED!");
}

connection.onmessage = function(e) {
  var server_message = e.data;
  // put the data in a DOM element to see
  document.getElementById("frank").innerHTML = server_message;
  var value = parseFloat(server_message);
  update_graph(value);
}

//connection.send("I have connected!");

function update_graph(value) {

  var graph = document.getElementById("graph");  // get the graph from the DOM
  var graph_context = graph.getContext("2d");    // get the graph's context
  var width = graph.width;                       // store width to improve performance
  var height = graph.height;                     // store height to imrpove performance
  var half_height = height / 2;                  // store height/2 to improve performance

  point_queue.push(value);
  q_size += 1;
  if(q_size > width){
    point_queue.shift(); // remove the oldest value - MAY be an O(N) operation, which is bayd, mmkay?
    q_size -= 1;
  }

  // console.log("Clearing graph");

  graph_context.clearRect(0, 0, width, height); // clear the graph on each update
  graph_context.strokeStyle="#FF0000";
  graph_context.moveTo(0, point_queue[0]);  
  graph_context.beginPath();

  // loop through points in the "queue", adding them to our path
  for(i = 1; i < q_size; i++){
    graph_context.lineTo(i, half_height - (point_queue[i] * half_height));
  } 

  // make the path visible
  graph_context.stroke();
}
