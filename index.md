---
layout: default
title: Accueil
---

<section class="presentation">
  <h1>{{ site.title }}</h1>
  <p>{{ site.description }}</p>
  <p>Cette lettre circule par courriel, sans passer par les réseaux sociaux. Chaque numéro reste consultable ici, et le <a href="{{ '/feed.xml' | relative_url }}">flux RSS</a> permet de la suivre depuis n'importe quel lecteur de flux.</p>
</section>

<section id="inscription" class="encart-inscription">
  <h2>S'abonner</h2>
  <p>L'inscription se fait par un simple courriel. Le lien ci-dessous ouvre votre messagerie avec un message prérempli ; il suffit de l'envoyer.</p>
  <p><a class="bouton" href="mailto:{{ site.email_contact }}?subject=Inscription%20%C3%A0%20la%20lettre&amp;body=Je%20souhaite%20recevoir%20la%20lettre%20d%27information%20%C3%A0%20cette%20adresse.">Recevoir la lettre par courriel</a></p>
  <p class="petit">Votre adresse sert uniquement à l'envoi de la lettre. Désinscription en un clic depuis chaque numéro. <a href="{{ '/confidentialite/' | relative_url }}">En savoir plus</a>.</p>
</section>

<section id="archives">
  <h2>Archives</h2>
  {% if site.posts.size > 0 %}
  <ul class="liste-lettres">
    {% for lettre in site.posts %}
    <li>
      <span class="date">{{ lettre.date | date: "%d/%m/%Y" }}</span>
      <a href="{{ lettre.url | relative_url }}">{{ lettre.title }}</a>
      {% if lettre.chapo %}<p>{{ lettre.chapo }}</p>{% endif %}
    </li>
    {% endfor %}
  </ul>
  {% else %}
  <p>Le premier numéro paraîtra prochainement.</p>
  {% endif %}
</section>
