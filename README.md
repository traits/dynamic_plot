dynamic-plot
============

Pelican plugin for embedding custom CSS and JS related to [D3](https://d3js.org/) and [three.js](https://threejs.org/) into individual Pelican blog articles. 

How
---
To install the plugin, [follow the instructions on the Pelican plugin page.](https://github.com/getpelican/pelican-plugins) My settings: 

```python
PLUGINS = ['dynamic_plot']
```

Next, create ```js``` and ```css``` directories in your ```content``` directory: 
```
website/
├── content
│   ├── js/
│   │   └── d3_vis_1.js
│   │   └── d3_vis_2.js
│   ├── css/
│   │   └── d3_styles.css
│   ├── article1.rst
│   ├── cat/
│   │   └── article2.md
│   └── pages
│       └── about.md
└── pelican.conf.py
```

and then add each resource as a comma-separated file name in the ```Scripts``` and ```Styles``` tags: 
```
Title: Using D3.js and three.js
Date: 2020-04-16 12:40:06
Category: blog
Summary: The (limited) return of the scripter...
Dynamic_plot: true
Tags: d3
Scripts: leibniz_d3.js, sphere_three.js
Styles: leibniz_d3.css
```

The ```dynamic_plot:``` tag is a convenience method that will load a minified version of D3. All of the JS and CSS will live in corresponding ```js``` and ```css``` folders in your ```output``` folder. 

Finally, in your base template (likely named ```base.html```), you need to add the following in your ```head``` tags: 
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

Using D3 in a Blog Post
-----------------------
With Markdown, this is pretty easy. Just add the raw HTML for your chart element in the middle of your markdown text: 

```
This is going to be a blog post about D3. Here is my chart: 

<div class="d3-chart"></div>

Isn't that a nice looking chart up there?
```

Then with D3, make sure you're selecting that element: 

```javascript
var svg = d3.select(".d3-chart").append("svg")
```

Ensure that your D3 is loaded *after* your body tags (as outlined above) so that it selects an existing element on the page. 
