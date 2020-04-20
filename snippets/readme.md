## Placeholders

Example D3 script containing a helper function for saving rendered content as browser download (JavaScript doesn't allow local file system access). This can be used as placeholder.

#### TODO

- Embedding style automatically in created svg (see `test_01.svg`)
- Creating scripting switch in output:
    ```
    <noscript>
    <img src="http://localhost:8000/images/test_01.svg"/>
    </noscript> 
    [...]
    </body>
    <script src="http://localhost:8000/js/leibniz_d3.js"></script>
    </html>
    ```
- extend functionality to three.js ([utilizing THREE.SVGRenderer?](https://threejs.org/docs/#examples/en/renderers/SVGRenderer))
- more configuration and automation regarding the Pelican workflow