---
title: Beer website
---

# Beer Website!

If you can see this, it's working!

<ul>
    {% for beer_hash in site.data.beer %}
    {% assign beer = beer_hash[1] %}
    <li>
        <h2>{{ beer.name }}</h2>
        <p>{{ beer.description }}</p>
    </li>
    {% endfor %}
</ul>
