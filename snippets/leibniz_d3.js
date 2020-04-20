var w = 500,
    h = 500,
    p = [20, 20, 40, 40],
    x = d3.scaleLinear().domain([2.5, 4]).range([0, w]),
    y = d3.scaleLinear().domain([-2, 2]).range([h, 0]),
    arc = [],
    n = 50,
    v = 0;

for (var i=0; i<n; i++) {
  var d = 1 + i * 2,
      s = i % 2 == 0 ? 1 : -1,
      dv = s * 4 / d;
  v += dv;
  if (i) arc.push("A", dv = Math.abs(dv), dv, 0, 0, 0);
  else arc.push("M");
  arc.push(x(v), y(0));
}

var vis = d3.select(".leibniz-spiral").append("svg")
    .attr("width", w + p[1] + p[3])
    .attr("height", h + p[0] + p[2])
    .append("g")
    .attr("transform", "translate(" + p[3] + "," + p[0] + ")");

vis.append("g")
    .attr("class", "x axis")
    .attr("transform", "translate(0," + y(0) + ")")
    .call(d3.axisBottom(x));

vis.append("path")
    .attr("class", "spiral")
    .attr("d", arc.join(" "));

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

saveSvg(vis.node().parentNode, 'test_01.svg')