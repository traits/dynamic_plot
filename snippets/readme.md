## Placeholders

This directory contains an example D3 script, containing a helper function for saving a D3-rendered scene by browser download (JavaScript doesn't allow local file system access). This can be used as placeholder for strict script-less requirements.

The replacement part is working yet in preliminary form:

`example.md:`
```
<noscript>
  <div><img src="{static}/images/leibniz_d3.svg" style="width:560; height:560;"/></div>
</noscript>
<div class="leibniz-spiral" style="width:960px; height:400px;"></div>
```

#### TODO

- embedding separate css style automatically into saved svg (see [`leibniz_d3.svg`](./leibniz_d3.svg) for a result, which was created manually from D3 svg output and [`leibniz_d3.css`](./leibniz_d3.css))
- support for local D3 and three.js installations
     
  `example.md`:
    ``` 
    title: Dynamic Example
    summary: ...
    dynamic_plots: all   
    d3_root:    https://d3js.org/
    d3_master:  d3.v4.min.js                # implemented
    three_root: https://threejs.org/build/    
    three_master: three.min.js
    place_holders: false,
    ``` 

- extend placeholder functionality to three.js ([SVGRenderer?](https://threejs.org/docs/#examples/en/renderers/SVGRenderer) [, exporter?](https://github.com/elifitch/three-svg-export/blob/master/src/index.js))
- generally more configuration and automation regarding the Pelican workflow
