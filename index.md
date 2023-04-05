---
title: Beer website
---
<div class="container">
{% for beer in site.beer | sort: "name" %}
<div class="card mb-3" style="max-width: 540px;">
<div class="row">
<h5 class="card-title">{{ beer.name }}</h5>
</div>
<div class="row g-0">
    <div class="col-3">
    {% assign path = beer.slug | prepend: "/beer-final/240/" | append: ".jpg"  %}
    {% assign file_exists = site.static_files | where: "path", path  %}
    {% if file_exists.size != 0 %}
    <img src="{{ path }}" class="img-fluid rounded-start">
    {% endif %}
    {% if beer.trappist == true %}
        <img src="/f/trappist.png" alt="Authentic Trappist Product" class="img-fluid rounded-start">
    {% endif %}
    </div>
    <div class="col-9">
    <div class="card-body">
        <p class="card-text">{{ beer.description }}</p>
        <!--<p class="card-text"><small class="text-body-secondary">Last updated 3 mins ago</small></p>-->
    </div>
    </div>
</div>
</div>
{% endfor %}
</div>

