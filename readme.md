## dynamic_plot

Pelican plugin for embedding custom [D3](https://d3js.org/) and [three.js](https://threejs.org/) scripts and associated CSS. This is a rewrite/extension of [Rob Story's plugin](https://github.com/wrobstory/pelican_dynamic). A live example can be found [here.](https://depot.traits.de/articles/2020/04/16-using-d3-and-threejs.html#using-d3-and-threejs)

### How

To install the plugin, follow the instructions on the [Pelican plugin page.](https://github.com/getpelican/pelican-plugins): 


`pelicanconf.py`:
```python
PLUGINS = ['dynamic_plot']

DYNAMIC_PLOT_OPTIONS = {
    # 'dynplot_d3_url' : 'https://d3js.org/d3.v5.min.js' (default) 
    # 'dynplot_three_url' : 'https://threejs.org/build/three.min.js' (default) 
}
```

and then add each resource as a comma-separated file name in the `dynplot_scripts` and `dynplot_styles` tags: 
```
title: Using D3.js and three.js
date: 2020-04-16
summary: D3 and three.js usage...
dynplot_d3_url: https://d3js.org/d3.v4.js
dynplot_scripts: leibniz_d3.js, sphere_three.js
dynplot_styles: leibniz_d3.css
```

- `dynplot_d3_url`: (default: `'https://d3js.org/d3.v5.min.js'`)  
- `dynplot_three_url`: (default: `'https://threejs.org/build/three.min.js'`)  
- `dynplot_scripts`:  The users script files for this blog entry
- `dynplot_styles`:  The users CSS files for this blog entry  

Options are evaluated with increasing priority: defaults -> pelican.conf -> article/page. Currently no local installations of the two JavaScript libraries are supported. All JS and CSS will be copied to `output` folder. Here, a leading forward slash for filenames in `dynplot_sripts` means, that the root directory is the `output` directory. Otherwise the path is considered relative to the respective article or page. 


Finally, in your base template (likely named `base.html`), you need to add the following in your `head` tags: 
```
{% if article %}
    {% if article.dynplot_styles %}
        {% for style in article.dynplot_styles %}
{{ style }}
        {% endfor %}
    {% endif %}
{% endif %}
```
and the following *after* the closing `</body>` and before `</html>`: 
```
{% if article %}
    {% if article.dynplot_scripts %}
        {% for script in article.dynplot_scripts %}
{{ script }}
        {% endfor %}
    {% endif %}
{% endif %}
```
The same can be done for pages.

Using D3 or/and three.js in a Blog Post
---------------------------------------
With Markdown, this is pretty easy. Just add the raw HTML for your chart element in the middle of your markdown text: 

```
D3 plot in blog post: 

<div class="leibniz-spiral" style="width:960px; height:400px;"></div>

... and three graphics:

<div class="three-sphere" style="width:600px; height:400px;"></div>
```

Then within your D3 script, make sure you're selecting that element: 

```javascript
var svg = d3.select(".leibniz-spiral").append("svg")
```
or if using three:
```javascript
var el = document.querySelector('.three-sphere');
el.appendChild(renderer.domElement);
```

Ensure that your js files are loaded *after* your body tags (as outlined above) so that it selects an existing element on the page. 


TODO
----

- Support of stricter non-scripting policies by [semi-]automatically created placeholders. 
- Supporting local D3 and three.js installations

Refer to [snippets/readme.md](snippets/readme.md) for additional information.
