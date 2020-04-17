dynamic_plot
============

Pelican plugin for embedding custom CSS and JS related to [D3](https://d3js.org/)(v4) and [three.js](https://threejs.org/) into individual Pelican blog articles. 

How
---
To install the plugin, [follow the instructions on the Pelican plugin page.](https://github.com/getpelican/pelican-plugins): 


`pelicanconf.py`:
```python
PLUGINS = ['dynamic_plot']
```

Next, create ```js``` and ```css``` directories in your ```content``` directory: 
```
website/
├── content
│   ├── js/
│   │   └── d3_example.js
│   │   └── three_example.js
│   ├── css/
│   │   └── d3_styles.css
│   ├── articles/
│   │   └── article.md
│   └── pages
│       └── about.md
└── pelicanconf.py
```

and then add each resource as a comma-separated file name in the ```Scripts``` and ```Styles``` tags: 
```
Title: Using D3.js and three.js
Date: 2020-04-16
Category: blog
Summary: D3 and three.js usage...
Dynamic_plot: true
Scripts: leibniz_d3.js, sphere_three.js
Styles: leibniz_d3.css
```

For ```dynamic_plot:true``` D3 and three processing for this article will be turned on. All of the JS and CSS will be copied in corresponding ```js``` and ```css``` folders in your ```output``` folder. 

Finally, in your base template (likely named ```base.html```), you need to add the following in your ```head``` tags. The same can be done for pages: 
```
{% if article %}
    {% if article.styles %}
        {% for style in article.styles %}
{{ style }}
        {% endfor %}
    {% endif %}
{% endif %}
```
and the following *after* your ```body``` tags: 
```
{% if article %}
    {% if article.scripts %}
        {% for script in article.scripts %}
{{ script }}
        {% endfor %}
    {% endif %}
{% endif %}
```

Using D3 or/and three.js in a Blog Post
------------------------------------
With Markdown, this is pretty easy. Just add the raw HTML for your chart element in the middle of your markdown text: 

```
This is going to be a blog post about D3. Here is my chart: 

<div class="dyn-plot"></div>

```

Then with D3, make sure you're selecting that element: 

```javascript
var svg = d3.select(".dyn-plot").append("svg")
```
or in three:
```javascript
var el = document.querySelector('.dyn-plot');
el.appendChild(renderer.domElement);
```


Ensure that your js files are loaded *after* your body tags (as outlined above) so that it selects an existing element on the page. 
