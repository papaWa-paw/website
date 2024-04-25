{% extends 'base.html' %}

{% block title %}
GG
{% endblock %}

{% block body %}
<div>
  <h3 class="title">{{ recipe.title }}</h3>
  <td width="60%">
	  <div id="ib_s_e_3" class="ib_s_e in_seen" data-in_c_id="ingridients" data-in_view_el="3"></div>
	  <table class="ingr" align="center">
		  <tbody><tr>
			  <td colspan="3" class="padding_l ingr_title">
				  <span class="prod">Продукты </span></td>
		  </tr>
		  <tr class="ingr_tr_0">
			  <td colspan="3" class="padding_l padding_r"><span class="">Лаваш тонкий - 1 лист</span></td>
		  </tr><tr class="ingr_tr_1">
			  <td colspan="3" class="padding_l padding_r"><span class="">Сыр (какой вам нравится) - 150 г</span></td>
		  </tr><tr class="ingr_tr_0">
			  <td colspan="3" class="padding_l padding_r"><span class="">Чеснок - 0,5-1 зубчик</span></td>
		  </tr><tr class="ingr_tr_1">
			  <td colspan="3" class="padding_l padding_r"><span class="">Зелень свежая, измельченная - 1-2 ст. ложки</span></td>
		  </tr><tr class="ingr_tr_0">
			  <td colspan="3" class="padding_l padding_r"><span class="">Яйцо - 1 шт.</span></td>
		  </tr><tr class="ingr_tr_1">
			  <td colspan="3" class="padding_l padding_r"><span class="">Сухари панировочные</span></td>
		  </tr><tr class="ingr_tr_0">
			  <td colspan="3" class="padding_l padding_r"><span class="">Масло растительное - для жарки</span></td>
		  </tr></tbody></table>
  </td>
</div>
{% endblock %}
