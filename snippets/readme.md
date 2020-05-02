## Placeholders

This directory contains an example D3 script, containing a helper function for saving a D3-rendered scene by browser download (JavaScript doesn't allow local file system access). This can be used as placeholder for strict script-less requirements.

Straightforward placeholding can be done independently of this simply by including a suiting prepared image.:

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
    dynplot_d3_url:  https://d3js.org/d3.v4.min.js  # implemented
    dynplot_scripts: (a.js, a_placeholder.svg),...  # tuples possible? 
    ``` 

- extend placeholder functionality to three.js ([SVGRenderer,](https://threejs.org/docs/#examples/en/renderers/SVGRenderer) [ three-svg-export?](https://github.com/elifitch/three-svg-export)) 
- generally more configuration and automation regarding the Pelican workflow
