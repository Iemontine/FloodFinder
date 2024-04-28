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


document.getElementById('cityInput').addEventListener('input', function() {
    if (this.value === '') { this.classList.add('placeholder');}
    else {this.classList.remove('placeholder');}
});


function displayingOutput() {
    var section = document.getElementById('outputSection');
    if (section.style.display == 'none') {
        section.style.display = "block";
    } else {
        section.style.display = "none";
    }
}


/* Notes:
- Write something for: If detect button is selected but there's nothing inside cityInput, display whatever you'd display if "check flood status" was pressed
- Load in data specific depending on which button is pressed
*/
