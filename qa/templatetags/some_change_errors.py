from django import template

register = template.Library()

@register.filter(name='beautify_errors')
def beautify_errors(errors):
    t = template.Template('''
        {% if errors %}
        <ul class="errors alert-error" style="color:red;">
            {% for value in errors.itervalues %}
                <li>{{ value|join:',' }}</li>
            {% endfor %}
        </ul>
        {% endif %}
        ''')
    c = template.Context(dict(errors=errors))
    return t.render(c)