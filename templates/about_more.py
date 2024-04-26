{% extends 'base.html' %}

{% block title %}
GG
{% endblock %}

{% block body %}
<div>
  <h2 class="title_more">{{ recipe.title }}</h2>
	<div class="author">
		<h1>{{ author.name }}</h1>
	</div>
	<div class="ingredient">
	  <table class="ingr">
		  <span class="prod"><h4><em>Продукты</em></h4></span>
		  <hr class="my-4" width="200px">
		  <div class="ingr">
		  {%  for i in recipe.ingredients.split('\r\n') %}
		  <tr class="ingr_tr_0">
			  <td colspan="3" class="padding_l padding_r"><span class="">{{ i }}</span></td>
		  {% endfor %}
		  </div>
	  </table>
	</div>
	<div class="description">
		{{ recipe.description }}
	</div>

	<div class="cooking">
		<h4><em>Процесс готовки</em></h4>
		<hr class="my-4" width="200px">
		<div class="cook">
		  {%  for r in recipe.cooking.split('\r\n') %}
		  <tr class="ingr_tr_0">
			  <td colspan="3" class="padding_l padding_r"><span>{{ r }}</span></td>
		  {% endfor %}
		</div>
	</div>
</div>
{% endblock %}
