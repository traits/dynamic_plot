## Placeholders

Example D3 script containing a helper function for saving rendered content as browser download (JavaScript doesn't allow local file system access). This can be used as placeholder for strict script-less requirements.

#### TODO

- embedding style automatically in created svg (see `leibniz_d3.svg`)
- creating scripting switch in output:
    ```
    <noscript>
    <img src="http://www.example.com/images/leibniz_d3.svg"/>
    </noscript> 
    [...]
    </body>
    <script src="http://www.example.com/js/leibniz_d3.js"></script>
    </html>
    ```
    or even finer granulation: 
    
    - script-only, noscript-only variants
      - configured as Pelican tag in markdown file
      - configured as container attribute for individual embeddings; `example.md` :
          
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
- more configuration and automation regarding the Pelican workflow
- configure maintenance local d3/three css