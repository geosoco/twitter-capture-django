from django import template

register = template.Library()

@register.inclusion_tag('form_base.html')
def bsform(form):
	return {'form': form}

