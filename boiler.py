#!/usr/bin/env python3
import sys

def die(message):
    sys.stderr.write(f"{message}\n")
    sys.exit(1)

try:
    import click
except ImportError:
    die("Required package Click is not installed")
try:
    import jinja2
except ImportError:
    die("Required package jinja2 is not installed")
try:
    from pathlib import Path
except ImportError:
    die("pathlib not available: probably need python 3.5 or higher")

import json
from json import JSONDecodeError

BOILER_TEMPLATE = """<!DOCTYPE html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial_scale=1">
    <title>{% block doctitle %}{% endblock doctitle %}</title>
    {% if boiler_use_bootstrap_css %}
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.2/css/bootstrap.min.css" integrity="sha384-Smlep5jCw/wG7hdkwQ/Z5nLIefveQRIY9nfy6xoR1uRYBtpZgI6339F5dgvm/e9B" crossorigin="anonymous">
    {% endif %}
    {% block extrahead %}
    {% endblock extrahead %}
    </head>
<body>
{% if boiler_use_bootstrap_css %}
    <div class="container">
{% endif %}
{% block content %}
{% endblock content %}
{% if boiler_use_bootstrap_css %}
</div>
{% endif %}
{% if boiler_use_jquery or boiler_use_bootstrap_js %}
    <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
{% endif %}
{% if boiler_use_bootstrap_js %}
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.3/umd/popper.min.js" integrity="sha384-ZMP7rVo3mIykV+2+9J3UJ46jBk0WLaUAdn689aCwoqbBJiSnjAK/l8WvCWPIPm49" crossorigin="anonymous"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.1.2/js/bootstrap.min.js" integrity="sha384-o+RDsa0aLu++PJvFqy8fFScvbHFLtbvScb8AjopnFD+iEQ7wo/CG0xlczd+2O/em" crossorigin="anonymous"></script>
{% endif %}
{% block extrajs %}
{% endblock extrajs %}
</body>
"""

@click.command()
@click.option('--extend-base-template', '-e', is_flag=True, default=False)
@click.option('--use-bootstrap', '-b',
              type=click.Choice(
                  ['none','css','js','both']
              ),
              default='none')
@click.option('--use-jquery', '-j', is_flag=True, default=False)
@click.option('--read-csv', '-c', is_flag=True, default=False)
@click.option('--read-tsv', is_flag=True, default=False)
@click.option('--template', '-t', type=click.File('r'))
@click.argument('data', type=click.File('r'), default="-")
@click.argument('output', type=click.File('w'), default="-")
def render_it(extend_base_template, use_bootstrap, use_jquery,
              read_csv, read_tsv,
                template, data, output):
    templates = {'base.html': BOILER_TEMPLATE}
    base_template = '{% extends "base.html" %}\n' if extend_base_template else ''

    if template:
        templates['child.html'] = f"{base_template}{template.read()}"

    loader = jinja2.DictLoader(templates)

    env = jinja2.Environment(
        loader=loader,
        trim_blocks=True,
        lstrip_blocks=True,
    )

    env.globals = dict(
        boiler_use_bootstrap_css = (use_bootstrap == "both") or (use_bootstrap == "css"),
        boiler_use_bootstrap_js =(use_bootstrap == "both") or (use_bootstrap == "js"),
        boiler_use_jquery = (use_jquery == True),
    )

    data_ext = Path(data.name).suffix

    if read_csv or read_tsv or data_ext == '.csv' or data_ext == '.tsv':
        import csv
        sniff = data.read(1024)
        data.seek(0)
        if '\t' in sniff or data_ext == '.tsv' or read_tsv:
            dia = csv.excel_tab
        else:
            dia = csv.excel
        reader = csv.DictReader(data, dialect=dia)
        input_data = {'csv':[item for item in reader]}
    else:
        raw_json = data.read()
        try:
            input_data = json.loads(raw_json)
        except JSONDecodeError:
            input_data = {}

    template_name = 'child.html' if 'child.html' in templates else 'base.html'
    t = env.get_template(template_name)
    output.write(t.render(**input_data))

if __name__ == "__main__":
    render_it()
