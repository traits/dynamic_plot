dynamic_plot
============

Pelican plugin for embedding custom CSS and JS related to [D3](https://d3js.org/) and [three.js](https://threejs.org/) into individual Pelican blog articles. This is a rewrite/extension of [Rob Story's plugin](https://github.com/wrobstory/pelican_dynamic). Live example [here.](https://depot.traits.de/articles/2020/04/16-using-d3-and-threejs.html#using-d3-and-threejs)

How
---
To install the plugin, follow the instructions on the [Pelican plugin page.](https://github.com/getpelican/pelican-plugins): 


`pelicanconf.py`:
```python
PLUGINS = ['dynamic_plot']
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

and then add each resource as a comma-separated file name in the `scripts` and `styles` tags: 
```
title: Using D3.js and three.js
date: 2020-04-16
category: blog
summary: D3 and three.js usage...
dynamic_plot: true
d3_script: d3.v5.min.js
scripts: leibniz_d3.js, sphere_three.js
styles: leibniz_d3.css
```

- `dynamic_plot` (default `None`): 
  
  If `true`, D3 and three processing for this article will be turned on. All of the JS and CSS will be copied in corresponding `js` and `css` folders in your `output` folder. 

- `d3_script` (default: `'d3.v4.min.js'`): 
  
  Changes the D3 variant at article level into `f'https://d3js.org/{d3_script}'`. 

Finally, in your base template (likely named `base.html`), you need to add the following in your `head` tags: 
```
{% if article %}
    {% if article.styles %}
        {% for style in article.styles %}
{{ style }}
        {% endfor %}
    {% endif %}
{% endif %}
```
and the following *after* the closing `</body>` and before `</html>`: 
```
{% if article %}
    {% if article.scripts %}
        {% for script in article.scripts %}
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
