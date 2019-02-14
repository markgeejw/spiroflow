// Script to control sensors and charts

// States
var hover = false;
var connected = false;
var flowing = false;

// Initializing global variables
// Variables for MQTT
var host = "test.mosquitto.org";
var port = 8080;
var topic = "IC.embedded/benchpsu"
// Variables for flow data
var breathCount = 0;
var volume = 0;
var volumeArray = [];
var peakFlow = 0;
var maxVolume = 0;
var negativeCount = 0;
// Array to hold values for charts
var flowVals = []; 
var volVals = []; 
var flowLabels = [];

// Initialise data structures
for(i = 0; i < 51; i++){
	flowVals.push(0);
	volVals.push(0);
	flowLabels.push(i*0.1);
}

var flowButton = document.getElementById("flow-btn");
var breathCountHTML = document.getElementById("breath-count");
var cancelFlow = document.getElementById("cancel-flow");
var spiroImg = document.getElementById("spiroflow-img");

function setHoverNotFlowConnected(){
  flowButton.className = "flow-btn-hover";
  breathCountHTML.className = "d-none";
  cancelFlow.className = "d-none";
  spiroImg.className = "";
}

function setHoverNotFlowNotConnected(){
  flowButton.className = "bg-danger";
  breathCountHTML.className = "d-none";
  cancelFlow.className = "d-none";
  spiroImg.className = "";
}

function setHoverFlow(){
  flowButton.className = "bg-danger";;
  breathCountHTML.className = "d-none";
  cancelFlow.className = "";
  spiroImg.className = "d-none";
}

function setNotHoverFlow(){
  flowButton.className = "bg-primary";
  breathCountHTML.className = "";
  cancelFlow.className = "d-none";
  spiroImg.className = "d-none";
}

function setNotHoverNotFlowNotConnected(){
  flowButton.className = "bg-danger";
  breathCountHTML.className = "d-none";
  cancelFlow.className = "d-none";
  spiroImg.className = "";
}

function setNotHoverNotFlowConnected(){
  flowButton.className = "bg-light";
  breathCountHTML.className = "d-none";
  cancelFlow.className = "d-none";
  spiroImg.className = "";
}

// Setup hover cancel effect for flow button
document.getElementById("flow-btn").onmouseenter = function(){
  hover = true;
  if (flowing == true){
    setHoverFlow();
  } else {
    if (connected){
      setHoverNotFlowConnected();
    } else {
      setHoverNotFlowNotConnected();
    }
  }
}

document.getElementById("flow-btn").onmouseleave = function(){
  hover = false;
  if (flowing == true){
    setNotHoverFlow();
  } else {
    if (connected){
      setNotHoverNotFlowConnected();
    } else {
      setNotHoverNotFlowNotConnected();
    }
  }
}

// Initialise graphs
var flowSpeechCtx = document.getElementById("flowSpeedChart");
var totalVolCtx = document.getElementById("totalVolChart");

var flowSpeedChart = new Chart(flowSpeechCtx, {
	responsive: true,
	type: 'line',
	data: {
		labels: flowLabels,
		datasets: [{
            label: "Flow Rate",
            lineTension: 0.3,
            backgroundColor: "rgba(78, 115, 223, 0.05)",
            borderColor: "rgba(78, 115, 223, 1)",
            pointRadius: 3,
            pointBackgroundColor: "rgba(78, 115, 223, 1)",
            pointBorderColor: "rgba(78, 115, 223, 1)",
            pointHoverRadius: 3,
            pointHoverBackgroundColor: "rgba(78, 115, 223, 1)",
            pointHoverBorderColor: "rgba(78, 115, 223, 1)",
            pointHitRadius: 10,
            pointBorderWidth: 2,
			data: flowVals
		}]
	},
	options: {
		responsive: true,
        maintainAspectRatio: false,
        layout: {
          padding: {
            left: 10,
            right: 25,
            top: 25,
            bottom: 0
          }
        },
        scales: {
        	xAxes: [{
        		display: true,
        		scaleLabel:{
        			display: true,
        			labelString: "Time (s)"
        		},
                time: {
                  unit: 'time'
                },
                gridLines: {
                  display: false,
                  drawBorder: false
                },
                ticks: {
                  maxTicksLimit: 7
                }
        	}],
            yAxes: [{
            	display: true,
            	type: 'linear',
            	scaleLabel:{
        			display: true,
        			labelString: "Flow Rate (m/s)"
        		},
                ticks: {
                  maxTicksLimit: 5,
                  padding: 10,
                  min: -1.0,
                  max: 3.0
                },
                gridLines: {
                  color: "rgb(234, 236, 244)",
                  zeroLineColor: "rgb(234, 236, 244)",
                  drawBorder: false,
                  borderDash: [2],
                  zeroLineBorderDash: [2]
                }
            }]
        },
        legend:{
        	display: false
        },
        title:{
        	display: true,
        	text: 'Flow Rate Chart'
        },
        tooltips: {
            backgroundColor: "rgb(255,255,255)",
            bodyFontColor: "#858796",
            titleMarginBottom: 10,
            titleFontColor: '#6e707e',
            titleFontSize: 14,
            borderColor: '#dddfeb',
            borderWidth: 1,
            xPadding: 15,
            yPadding: 15,
            displayColors: false,
            intersect: false,
            mode: 'index',
            caretPadding: 10
        }
    }
})
var totalVolChart = new Chart(totalVolCtx, {
	responsive: true,
	type: 'line',
	data: {
		labels: flowLabels,
		datasets: [{
            label: "Lung Volume",
            lineTension: 0.3,
            backgroundColor: "rgba(78, 115, 223, 0.05)",
            borderColor: "rgba(78, 115, 223, 1)",
            pointRadius: 3,
            pointBackgroundColor: "rgba(78, 115, 223, 1)",
            pointBorderColor: "rgba(78, 115, 223, 1)",
            pointHoverRadius: 3,
            pointHoverBackgroundColor: "rgba(78, 115, 223, 1)",
            pointHoverBorderColor: "rgba(78, 115, 223, 1)",
            pointHitRadius: 10,
            pointBorderWidth: 2,
			data: volVals,
		}]
	},
	options: {
		responsive: true,
        maintainAspectRatio: false,
        layout: {
          padding: {
            left: 10,
            right: 25,
            top: 25,
            bottom: 0
          }
        },
        scales: {
        	xAxes: [{
        		display: true,
        		scaleLabel:{
        			display: true,
        			labelString: "Time (s)"
        		},
                time: {
                  unit: 'time'
                },
                gridLines: {
                  display: false,
                  drawBorder: false
                },
                ticks: {
                  maxTicksLimit: 7
                }
        	}],
            yAxes: [{
            	display: true,
            	type: 'linear',
            	scaleLabel:{
        			display: true,
        			labelString: "Volume (l)"
        		},
                ticks: {
                  maxTicksLimit: 5,
                  padding: 10,
                },
                gridLines: {
                  color: "rgb(234, 236, 244)",
                  zeroLineColor: "rgb(234, 236, 244)",
                  drawBorder: false,
                  borderDash: [2],
                  zeroLineBorderDash: [2]
                }
            }]
        },
        legend:{
        	display: false
        },
        title:{
        	display: true,
        	text: 'Lung Volume Chart'
        },
        tooltips: {
            backgroundColor: "rgb(255,255,255)",
            bodyFontColor: "#858796",
            titleMarginBottom: 10,
            titleFontColor: '#6e707e',
            titleFontSize: 14,
            borderColor: '#dddfeb',
            borderWidth: 1,
            xPadding: 15,
            yPadding: 15,
            displayColors: false,
            intersect: false,
            mode: 'index',
            caretPadding: 10
        }
    }
})

// Create a client instance
var client = new Paho.Client(host, port, "clientjslol");

// Set callback handlers
client.onConnectionLost = onConnectionLost;
client.onMessageArrived = onMessageArrived;

// Connect the client
client.connect({onSuccess:onConnect, reconnect: true});


// Called when the client connects
function onConnect() {
	// Once a connection has been made, make a subscription and send a message.
	console.log("Connected to MQTT");
	client.subscribe(topic);
	message = new Paho.Message("stop");
  message.destinationName = topic;
  connected = true;
  client.send(message);
  if (hover){
    if (flowing){
      setHoverFlow();
    } else {
      setHoverNotFlowConnected();
    }
  } else {
    if (flowing){
      setNotHoverFlow();
    } else {
      setNotHoverNotFlowConnected();
    }
  }
}

// Called when the client loses its connection
function onConnectionLost(responseObject) {
	if (responseObject.errorCode !== 0) {
		console.log("onConnectionLost:"+responseObject.errorMessage);
  }
}

// Called when a message arrives
function onMessageArrived(message) {
	messageStr = message.payloadString;
	messageWords = messageStr.split(" ");	

	if(messageStr.charAt(0) === 'f' && messageWords.length === 3){
    console.log(messageStr);
		flowData = messageWords[0].substr(1,);
		flowData = parseFloat(flowData);
		updateFlow(flowData);

		tempData = messageWords[1].substr(1,);
		tempData = parseFloat(tempData);
		updateTemp(tempData);

		humidityData = messageWords[2].substr(1,);
		humidityData = parseFloat(humidityData);
    updateHumidity(humidityData);
	}

}

// Add data to chart
function addData(chart, data){
	chart.data.datasets.forEach((dataset) =>{
		dataset.data.shift();
		dataset.data.push(data);
	});
	chart.update();
}

// Reset chart to all 0s
function resetFlow(){
	for(i=0; i < 51; i++){
		addData(flowSpeedChart, 0);
		addData(totalVolChart, 0);
	}
	volume = 0;
}

function toggleSensors(){
  if (!flowing) {
    initSensors()
  } else {
    killSensors()
  }
}

// Initialize sensors through MQTT messages
function initSensors(){
  console.log("Initializing sensors");
	message = new Paho.Message("start");
	message.destinationName = topic;
  client.send(message);
  flowing = true;
  breathCount++;
  breathCountHTML.innerHTML = breathCount.toString();
  setHoverFlow();
  cards = document.getElementsByClassName("read");
  for(i=0; i < cards.length; i++){
    cards[i].classList.remove("border-left-danger");
    cards[i].classList.remove("border-left-success");
    cards[i].classList.add("border-left-primary");
  }
}

function killSensors(){
  flowing = false;
  console.log("Stopping sensors");
	message = new Paho.Message("stop");
	message.destinationName = topic;
  client.send(message);
  if (hover){
    setHoverNotFlowConnected();
  } else {
    setNotHoverNotFlowConnected();
  }
  peakFlow = 0;
  breathCount = 0;
  volumeArray = [];
  cards = document.getElementsByClassName("read");
  for(i=0; i < cards.length; i++){
    cards[i].classList.remove("border-left-primary");
    cards[i].classList.add("border-left-danger");
  }
}

// Update functions for various values
function updateFlow(data){
  if (data > peakFlow){
    peakFlow = data;
  }
	addData(flowSpeedChart, data);
	if(data > 0 && negativeCount < 3){
		volume = volume + data * 0.125;
		addData(totalVolChart, volume);
	} else if (data < 0 && negativeCount < 3){
		negativeCount++;
		volume = volume + data * 0.2;
		addData(totalVolChart, volume);
	} else if (negativeCount >= 3){
		negativeCount = 0;
		if(maxVolume < volume){
			maxVolume = volume;
      volumeArray.push(maxVolume);
      maxVolume = 0;
			volume = 0;
      addData(totalVolChart, volume);
      breathCount++;
      document.getElementById("breath-count").innerHTML = breathCount.toString();
		}
  }
  if (breathCount > 3){
    averageVolume = volumeArray.reduce( (a,b) => a + b) / volumeArray.length;
    document.getElementById('rt-lung').innerHTML = parseFloat(averageVolume.toString()).toFixed(2);
    document.getElementById('rt-peak').innerHTML = parseFloat(peakFlow.toString()).toFixed(2);
    killSensors()
    cards = document.getElementsByClassName("read");
    for(i=0; i < cards.length; i++){
      cards[i].classList.remove("border-left-primary");
      cards[i].classList.remove("border-left-danger");
      cards[i].classList.add("border-left-success");
    }
  }
}

function updateTemp(data){
	document.getElementById('rt-temp').innerHTML = data.toString();
}

function updateHumidity(data){
	document.getElementById('rt-humidity').innerHTML = data.toString();
}