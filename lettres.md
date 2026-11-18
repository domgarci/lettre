---
layout: default
title: Ressources
permalink: /ressources/
theme: papier
---

# Ressources

Documents et numéros de la lettre, du plus récent au plus ancien. Pour les recevoir par courriel : [s'abonner]({{ '/a-propos/' | relative_url }}#inscription).

<div class="vignettes">
{% for lettre in site.posts %}
  <a class="vignette" href="{{ lettre.url | relative_url }}">
    <span class="vignette-meta">{% if lettre.numero %}N° {{ lettre.numero }} · {% endif %}{{ lettre.date | date: "%d/%m/%Y" }}</span>
    <strong>{{ lettre.title }}</strong>
    {% if lettre.chapo %}<span class="vignette-texte">{{ lettre.chapo }}</span>{% endif %}
  </a>
{% endfor %}
</div>

{% if site.posts.size == 0 %}<p>Le premier numéro paraîtra prochainement.</p>{% endif %}
