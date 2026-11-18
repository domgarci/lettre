---
layout: default
title: Lettres
permalink: /lettres/
theme: papier
---

# Lettres

Chaque numéro de la lettre, dans l'ordre de parution. Pour les recevoir par courriel : [s'abonner]({{ '/a-propos/' | relative_url }}#inscription).

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
