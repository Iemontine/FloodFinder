(function () {
	var globe = planetaryjs.planet();
	globe.loadPlugin(autorotate(10));
	globe.loadPlugin(planetaryjs.plugins.earth({
		topojson: { file: 'https://raw.githubusercontent.com/MadeByDroids/madebydroids.github.io/master/world-110m-withlakes%20(1).json' },
		oceans: { fill: '#718cb6' },
		land: { fill: '#bdc9db'},
		borders: { stroke: '#bdc9db' }
	}));
	globe.loadPlugin(lakes({
		fill: '#bdc9db'
	}));
	globe.loadPlugin(planetaryjs.plugins.pings());
	globe.projection.scale(300).translate([300, 300]).rotate([-100, -20, 0]);
	var colors = ['#97edd4', 'white', '#97edd4', 'white'];
	setInterval(function () {
		var lat = Math.random() * 170 - 85;
		var lng = Math.random() * 360 - 180;
		var color = colors[Math.floor(Math.random() * colors.length)];
		globe.plugins.pings.add(lng, lat, { color: '#00295e', ttl: 2000, angle: Math.random() * 10 });
	}, 1500);
	var canvas = document.getElementById('rotatingGlobe');
	if (window.devicePixelRatio == 2) {
		canvas.width = 1200;
		canvas.height = 1200;
		context = canvas.getContext('2d');
		context.scale(2, 2);
	}
	globe.draw(canvas);
	function autorotate(degPerSec) {
		return function (planet) {
			var lastTick = null;
			var paused = false;
			planet.plugins.autorotate = {
				pause: function () { paused = true; },
				resume: function () { paused = false; }
			};
			planet.onDraw(function () {
				if (paused || !lastTick) {
					lastTick = new Date();
				} else {
					var now = new Date();
					var delta = now - lastTick;
					var rotation = planet.projection.rotate();
					rotation[0] += degPerSec * delta / 1000;
					if (rotation[0] >= 180) rotation[0] -= 360;
					planet.projection.rotate(rotation);
					lastTick = now;
				}
			});
		};
	};
	function lakes(options) {
		options = options || {};
		var lakes = null;




		return function (planet) {
			planet.onInit(function () {
				// on its namespace on `planet.plugins`. We're loading a custom
				var world = planet.plugins.topojson.world;
				lakes = topojson.feature(world, world.objects.ne_110m_lakes);
			});




			planet.onDraw(function () {
				planet.withSavedContext(function (context) {
					context.beginPath();
					planet.path.context(context)(lakes);
					context.fillStyle = options.fill || 'black';
					context.fill();
				});
			});
		};
	};
})();


document.addEventListener('DOMContentLoaded', function () {
	const levels = [
		document.querySelector('header'),
		document.getElementById('floodStatusButton'),
		document.querySelector('.inputArea'),
		document.getElementById('outputSection')
	];


	globe = document.getElementById('rotatingGlobe');
	initialBottom = -200; // Initial bottom position of the globe


	levels.forEach((level, i) => {
		level.addEventListener('mouseenter', function () {
			newPosition = initialBottom + (50 * (i + 1));
			globe.style.bottom = `${newPosition}px`;
		});


		level.addEventListener('mouseleave', function () {
			globe.style.bottom = `${initialBottom}px`;
		});
	});
});


// Modify event listener for cityInputButton
document.getElementById('cityInputButton').addEventListener('click', function () {
	var city = document.getElementById('cityInput').value;
	getWeatherAndDisplay(city); // Call the API request function
});


// Add event listener for floodStatusButton
document.getElementById('floodStatusButton').addEventListener('click', function () {
	var city = document.getElementById('cityInput').value;
	getWeatherAndDisplay(city); // Reuse the same function for consistency
});


// Function to handle the API request
function getWeatherAndDisplay(city) {
	// Check if the city is not specified and set a default message
	if (!city) {
		document.getElementById('outputSection').innerHTML = 'Please enter a city to check its flood status or detect its weather conditions.';
		displayingOutput();
		return;
	}


	// Prepare the request
	var url = 'http://localhost:5000/getWeather'; // Change this URL to where your Python Flask API is hosted
	fetch(url, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
		},
		body: JSON.stringify({ location: city }),
	})
	.then(response => response.text())
	.then(data => {
		// Display the data in 'outputSection'
		document.getElementById('outputSection').innerHTML = data;
		var section = document.getElementById('map');
		section.style.display = "block";
		displayingOutput();
	})
	.catch((error) => {
		console.error('Error:', error);
		document.getElementById('outputSection').innerHTML = 'An error occurred while processing your request.';
		displayingOutput();
	});
}


document.getElementById('cityInput').addEventListener('input', function() {
	if (this.value === '') { this.classList.add('placeholder');}
	else {this.classList.remove('placeholder');}
});




function displayingOutput() {
	var section = document.getElementById('outputSection');
	section.style.display = "flex";

}


/* Notes:
- Write something for: If detect button is selected but there's nothing inside cityInput, display whatever you'd display if "check flood status" was pressed
- Load in data specific depending on which button is pressed
*/
