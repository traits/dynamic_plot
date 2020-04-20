## Placeholders

Example D3 script containing a helper function for saving a D3-rendered scene by browser download (JavaScript doesn't allow local file system access). This can be used as placeholder for strict script-less requirements.

The replacement part is working yet in preliminary form:

`example.md:`
```
<noscript>
  <div><img src="{static}/images/leibniz_d3.svg" style="width:560; height:560;"/></div>
</noscript>
<div class="leibniz-spiral" style="width:960px; height:400px;"></div>
```

#### TODO

- embedding separate css style automatically into created svg (see [`leibniz_d3.svg`](./leibniz_d3.svg) for a result, created manually from D3 svg output and [`leibniz_d3.css`](./leibniz_d3.css))
- finer scripting switch granulation in Pelican output during content creation: script-only, noscript-only variants:

    - configured as Pelican tag in markdown file
    - configured as container attribute for individual embeddings: 
     
  `example.md`:

      ``` 
      Title: Dynamic Example
      Summary: ...
      Dynamic_plot: true       #  this has to be rearranged
      Scripts: leibniz_d3.js   #             -"-
      Styles: leibniz_d3.css   #             -"-
      Output_strategy:         #  both/placeholder_only/dynamic_only?    

      [...]

      <div class="leibniz-spiral" class="placeholder_only" style=[...]></div>
      ```   

- extend functionality to three.js ([utilizing THREE.SVGRenderer?](https://threejs.org/docs/#examples/en/renderers/SVGRenderer))
- generally more configuration and automation regarding the Pelican workflow
- configure maintenance of local d3/three css