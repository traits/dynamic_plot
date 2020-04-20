//import { SVGRenderer } from './three/examples/jsm/renderers/SVGRenderer.js';
import { OrbitControls } from 'https://threejs.org/examples/jsm/controls/OrbitControls.js';


var unique_descriptor = '.three-sphere'

function createTextCanvas(text, color, font, size) {
    size = size || 16;
    var canvas = document.createElement('canvas');
    var ctx = canvas.getContext('2d');
    var fontStr = (size + 'px ') + (font || 'Arial');
    ctx.font = fontStr;
    var w = ctx.measureText(text).width;
    var h = Math.ceil(size);
    canvas.width = w;
    canvas.height = h;
    ctx.font = fontStr;
    ctx.fillStyle = color;
    ctx.fillText(text, 0, Math.ceil(size * 0.8));
    //var el = document.querySelector(unique_descriptor);
    //el.appendChild(canvas); 
    return canvas;
}

function createText2D(text, color, font, size, segW, segH) {
    var canvas = createTextCanvas(text, color, font, size);
    var plane = new THREE.PlaneGeometry(canvas.width, canvas.height, segW, segH);
    var tex = new THREE.Texture(canvas);
    tex.needsUpdate = true;
    var planeMat = new THREE.MeshBasicMaterial({
        map: tex,
        color: 0xffffff,
        transparent: true
    });
    var mesh = new THREE.Mesh(plane, planeMat);
    mesh.scale.set(0.5, 0.5, 0.5);
    mesh.doubleSided = true;
    return mesh;
}

// from http://stackoverflow.com/questions/5623838/rgb-to-hex-and-hex-to-rgb
function hexToRgb(hex) { //TODO rewrite with vector output
    var result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    return result ? {
        r: parseInt(result[1], 16),
        g: parseInt(result[2], 16),
        b: parseInt(result[3], 16)
    } : null;
}

var renderer = new THREE.WebGLRenderer({
    antialias: true
});
var w = 600;
var h = 400;
renderer.setSize(w, h);
renderer.setPixelRatio( window.devicePixelRatio );
var el = document.querySelector(unique_descriptor);
el.appendChild(renderer.domElement);

renderer.setClearColor(new THREE.Color(0xFFFFFF));

var camera = new THREE.PerspectiveCamera(45, w / h, 1, 10000);
camera.position.z = 200;
camera.position.x = -100;
camera.position.y = 100;

var scene = new THREE.Scene();
//scene.background = new THREE.Color( 0x444444 );

var controls = new OrbitControls( camera, renderer.domElement );

controls.enableDamping = true; // an animation loop is required when either damping or auto-rotation are enabled
controls.dampingFactor = 0.05;

controls.screenSpacePanning = false;

controls.minDistance = 100;
controls.maxDistance = 500;

var lights = [];
lights[ 0 ] = new THREE.PointLight( 0xffffff, 1, 0 );
lights[ 1 ] = new THREE.PointLight( 0xffffff, 1, 0 );
lights[ 2 ] = new THREE.PointLight( 0xffffff, 1, 0 );

lights[ 0 ].position.set( 0, 200, 0 );
lights[ 1 ].position.set( 100, 200, 100 );
lights[ 2 ].position.set( - 100, - 200, - 100 );

scene.add( lights[ 0 ] );
scene.add( lights[ 1 ] );
scene.add( lights[ 2 ] );

var scatterPlot = new THREE.Object3D();
scene.add(scatterPlot);

var sphere = new THREE.Group();
var geometry = new THREE.SphereGeometry( 35, 32, 32 );

var meshMaterial = new THREE.MeshPhongMaterial( { color: 0x156289,  opacity: 0.85, transparent: true, emissive: 0x072534 } );
var lineMaterial = new THREE.LineBasicMaterial( { color: 0x000099, linewidth: 1 } );

sphere.add( new THREE.Mesh( geometry, meshMaterial ) );
sphere.add( new THREE.LineSegments( geometry, lineMaterial ) );
scene.add( sphere );

scatterPlot.rotation.y = 0;

function v(x, y, z) {
    return new THREE.Vector3(x, y, z);
}

var radius = 50; 
var rext = d3.extent([-radius,radius])
var xExent = rext;
var yExent = rext;
var zExent = rext;

var vpts = {
    xMax: xExent[1],
    xCen: (xExent[1] + xExent[0]) / 2,
    xMin: xExent[0],
    yMax: yExent[1],
    yCen: (yExent[1] + yExent[0]) / 2,
    yMin: yExent[0],
    zMax: zExent[1],
    zCen: (zExent[1] + zExent[0]) / 2,
    zMin: zExent[0]
}

var colour = d3.schemeCategory20;
var lineMat = new THREE.LineBasicMaterial({
    color: 0x000000,
    linewidth: 1
});

function addLine(b, e)
{
    var lineGeo = new THREE.Geometry();
    lineGeo.vertices.push(
        b, e
    );
    
    var line = new THREE.Line(lineGeo, lineMat);
    line.type = THREE.LineSegments;
    scatterPlot.add(line);    
}

addLine(v(vpts.xMin, vpts.yMin, vpts.zMin), v(vpts.xMax, vpts.yMin, vpts.zMin))
addLine(v(vpts.xMin, vpts.yMin, vpts.zCen), v(vpts.xMax, vpts.yMin, vpts.zCen))
addLine(v(vpts.xMin, vpts.yMin, vpts.zMax), v(vpts.xMax, vpts.yMin, vpts.zMax))
addLine(v(vpts.xMin, vpts.yCen, vpts.zMin), v(vpts.xMax, vpts.yCen, vpts.zMin))
addLine(v(vpts.xMin, vpts.yCen, vpts.zCen), v(vpts.xMax, vpts.yCen, vpts.zCen))
addLine(v(vpts.xMin, vpts.yCen, vpts.zMax), v(vpts.xMax, vpts.yCen, vpts.zMax))
addLine(v(vpts.xMin, vpts.yMax, vpts.zMin), v(vpts.xMax, vpts.yMax, vpts.zMin))
addLine(v(vpts.xMin, vpts.yMax, vpts.zCen), v(vpts.xMax, vpts.yMax, vpts.zCen))
addLine(v(vpts.xMin, vpts.yMax, vpts.zMax), v(vpts.xMax, vpts.yMax, vpts.zMax))

addLine(v(vpts.xMin, vpts.yMin, vpts.zMin), v(vpts.xMin, vpts.yMax, vpts.zMin))
addLine(v(vpts.xMin, vpts.yMin, vpts.zCen), v(vpts.xMin, vpts.yMax, vpts.zCen))
addLine(v(vpts.xMin, vpts.yMin, vpts.zMax), v(vpts.xMin, vpts.yMax, vpts.zMax))
addLine(v(vpts.xCen, vpts.yMin, vpts.zMin), v(vpts.xCen, vpts.yMax, vpts.zMin))
addLine(v(vpts.xCen, vpts.yMin, vpts.zCen), v(vpts.xCen, vpts.yMax, vpts.zCen))
addLine(v(vpts.xCen, vpts.yMin, vpts.zMax), v(vpts.xCen, vpts.yMax, vpts.zMax))
addLine(v(vpts.xMax, vpts.yMin, vpts.zMin), v(vpts.xMax, vpts.yMax, vpts.zMin))
addLine(v(vpts.xMax, vpts.yMin, vpts.zCen), v(vpts.xMax, vpts.yMax, vpts.zCen))
addLine(v(vpts.xMax, vpts.yMin, vpts.zMax), v(vpts.xMax, vpts.yMax, vpts.zMax))

renderer.render(scene, camera);

var svg = createSvg(sphere, camera, renderer)
saveSvg(svg, 'sphere_three.svg')

var last = new Date().getTime();

function animate(t) {
    last = t;
    renderer.clear();
    camera.lookAt(scene.position);
    renderer.render(scene, camera);
    window.requestAnimationFrame(animate, renderer.domElement);
    controls.update(); 
};
animate(new Date().getTime());


function createSvg(pobj, camera, renderer) {
	const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
	const canvas = renderer.context.canvas;
	const raycaster = new THREE.Raycaster();
	const cameraPosition = camera.position.clone();
	//const vertices = obj.geometry.vertices
	let svgPolys = [];
	svg.setAttribute("viewBox", `0 0 ${canvas.width} ${canvas.height}`);
	pobj.updateMatrixWorld();

    pobj.children.forEach(function(obj) {
        if(obj.geometry){
        var vertices = obj.geometry.vertices
        if (obj.geometry.faces.length > 0){
        obj.geometry.faces.map(face => {
            face.centroid = faceCentroid(face, vertices);
            face.distance = face.centroid.distanceTo(cameraPosition);
            return face;
        })
        .sort(dynamicSort("distance"))
        .forEach(face => {
            let coords = {};
            let polygon = document.createElementNS('http://www.w3.org/2000/svg','polygon');

            coords.a = coordsFromVertex(vertices[face.a], camera, canvas);
            coords.b = coordsFromVertex(vertices[face.b], camera, canvas);
            coords.c = coordsFromVertex(vertices[face.c], camera, canvas);
            polygon.setAttribute("points", `${coords.a.x},${coords.a.y} ${coords.b.x},${coords.b.y} ${coords.c.x},${coords.c.y}`);
            polygon.style.stroke = '#000099' //hexColorAtPoint(face.centroid, camera, canvas, renderer);
            //polygon.setAttribute("shape-rendering", 'crispEdges')
            polygon.setAttribute("stroke-width", "0.02%") 
            polygon.style.fill = '#156289'
            polygon.style.opacity = 0.75
            svg.appendChild(polygon);
        });
}}});
    return svg;
}

function saveSvg(svgEl, name) {
    svgEl.setAttribute("xmlns", "http://www.w3.org/2000/svg");
    var svgData = svgEl.outerHTML;
    var preface = '<?xml version="1.0" standalone="no"?>\r\n';
    var svgBlob = new Blob([preface, svgData], {type:"image/svg+xml;charset=utf-8"});
    var svgUrl = URL.createObjectURL(svgBlob);
    var downloadLink = document.createElement("a");
    downloadLink.href = svgUrl;
    downloadLink.download = name;
    document.body.appendChild(downloadLink);
    downloadLink.click();
    document.body.removeChild(downloadLink);
}


function coordsFromVertex(vertex, camera, canvas) {
	const widthHalf = 0.5 * canvas.width;
	const heightHalf = 0.5 * canvas.height;
	const coord = vertex.clone().project(camera);
	coord.x = ( coord.x * widthHalf ) + widthHalf;
	coord.y = -( coord.y * heightHalf ) + heightHalf;
	return coord;
}

function faceCentroid(face, vertices) {
	const v1 = vertices[ face.a ];
	const v2 = vertices[ face.b ];
	const v3 = vertices[ face.c ];

	// calculate the centroid
	const centroid = new THREE.Vector3();
	centroid.x = ( v1.x + v2.x + v3.x ) / 3;
	centroid.y = ( v1.y + v2.y + v3.y ) / 3;
	centroid.z = ( v1.z + v2.z + v3.z ) / 3;
	return centroid;
}

function dynamicSort(property) {
    var sortOrder = -1;
    if(property[0] === "-") {
        sortOrder = -1;
        property = property.substr(1);
    }
    return function (a,b) {
        var result = (a[property] < b[property]) ? -1 : (a[property] > b[property]) ? 1 : 0;
        return result * sortOrder;
    }
}

function hexColorAtPoint(vector, camera, canvas, renderer) {
	const coord = vector.clone().project(camera);
	const widthHalf = 0.5 * canvas.width;
	const heightHalf = 0.5 * canvas.height;
	const gl = renderer.getContext();
	let pixel = new Uint8Array(4);

	coord.x = ( coord.x * widthHalf ) + widthHalf;
	coord.y = ( coord.y * heightHalf ) + heightHalf;
	gl.readPixels(coord.x, coord.y, 1, 1, gl.RGBA, gl.UNSIGNED_BYTE, pixel);

	let hex = "#" + ("000000" + rgbToHex(pixel[0], pixel[1], pixel[2])).slice(-6);
	return hex;
}

function rgbToHex(r, g, b) {
    if (r > 255 || g > 255 || b > 255) {
    	console.error("Invalid color component");
    }
    return ((r << 16) | (g << 8) | b).toString(16);
}
