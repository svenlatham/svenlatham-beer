---
title: Beer website
---

# Beer Website!

If you can see this, it's working!

<ul>
    {% for beer in site.beer %}
    <li>
        <h2><a href="{{ beer.url }}">{{ beer.name }}</a></h2>
        <p>{{ beer.description }}</p>
    </li>
    {% endfor %}
</ul>
