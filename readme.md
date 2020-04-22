## dynamic_plot

Pelican plugin for embedding custom CSS and JS related to [D3](https://d3js.org/) and [three.js](https://threejs.org/) into individual Pelican blog articles. This is a rewrite/extension of [Rob Story's plugin](https://github.com/wrobstory/pelican_dynamic). A live example can be found [here.](https://depot.traits.de/articles/2020/04/16-using-d3-and-threejs.html#using-d3-and-threejs)

### How

To install the plugin, follow the instructions on the [Pelican plugin page.](https://github.com/getpelican/pelican-plugins): 


`pelicanconf.py`:
```python
PLUGINS = ['dynamic_plot']

DYNAMIC_PLOT_OPTIONS = {
    # 'dynamic_plots': None (default), 'all', 'd3', 'three'
    # 'd3_master' : 'd3.v5.min.js' (default) 
}
```

Next, create `js` and `css` directories in your `content` directory: 
```
  site/
    ├── content
    │   ├── js/
    │   │   └── leibniz_d3.js
    │   │   └── sphere_three.js
    │   ├── css/
    │   │   └── leibniz_d3.css
    │   ├── articles/
    │   │   └── article.md
    │   └── pages
    │       └── about.md
    └── pelicanconf.py
```

and then add each resource as a comma-separated file name in the `dp_scripts` and `dp_styles` tags: 
```
title: Using D3.js and three.js
date: 2020-04-16
summary: D3 and three.js usage...
dynamic_plots: all
d3_master: d3.v4.js
dp_scripts: leibniz_d3.js, sphere_three.js
dp_styles: leibniz_d3.css
```

- `dynamic_plots` (default `None`): 
  
  Values: `None` (default), `'all'`, `'d3'`, `'three'` 

- `d3_master` (default: `'d3.v5.min.js'`): 
  
  Changes the D3 variant into `f'https://d3js.org/{d3_script}'`. 

Options are evaluated with increasing priority: defaults -> pelican.conf -> article/page. Processing occurs only if `dynamic_plots != None`. Currently no local installations of the two JavaScript libraries are supported. All of the JS and CSS will be copied in corresponding `js` and `css` folders in your `output` folder. 



Finally, in your base template (likely named `base.html`), you need to add the following in your `head` tags: 
```
{% if article %}
    {% if article.dp_styles %}
        {% for style in article.dp_styles %}
{{ style }}
        {% endfor %}
    {% endif %}
{% endif %}
```
and the following *after* the closing `</body>` and before `</html>`: 
```
{% if article %}
    {% if article.dp_scripts %}
        {% for script in article.dp_scripts %}
{{ script }}
        {% endfor %}
    {% endif %}
{% endif %}
```
The same can be done for pages.

Using D3 or/and three.js in a Blog Post
------------------------------------
With Markdown, this is pretty easy. Just add the raw HTML for your chart element in the middle of your markdown text: 

```
D3 plot in blog post: 

<div class="leibniz-spiral" style="width:960px; height:400px;"></div>

... and three graphics:

<div class="three-sphere" style="width:600px; height:400px;"></div>
```

Then with D3, make sure you're selecting that element: 

```javascript
var svg = d3.select(".leibniz-spiral").append("svg")
```
or in three:
```javascript
var el = document.querySelector('.three-sphere');
el.appendChild(renderer.domElement);
```

Ensure that your js files are loaded *after* your body tags (as outlined above) so that it selects an existing element on the page. 


TODO
----

Refer to [snippets/readme.md](snippets/readme.md) for additional information.
