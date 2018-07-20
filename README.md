# boiler

This tiny little package uses [Click](http://click.pocoo.org/) and
[Jinja2](http://jinja.pocoo.org/) to give you super fast, super basic
HTML pages, with or without several common addons. You can submit a JSON
file as input, and its keys and values will be used as the template
context.  Options are available to automatically add CDN-sourced versions
of Bootstrap (either its CSS or JS or both) and/or jQuery.  (If you ask
for the Bootstrap JS, jQuery and the `popper` library, which are
prerequisites, get added as well.)

You can install this package with the following `pip` command:

```shell
pip install -e git://github.com:phoikoi/boiler.git@v1.0#egg=boiler
```

### Usage

```
boiler [OPTIONS] [DATA] [OUTPUT]

Options:
  -e, --extend-base-template
  -b, --use-bootstrap [none|css|js|both]
  -j, --use-jquery
  -t, --template FILENAME
  --help                          Show this message and exit.
```

If you don't specify the `DATA` argument (the input JSON file, in
other words,) `boiler` will default to using `stdin`. Similarly, `OUTPUT` will default to `stdout`.

If you pass a template filename (which must be a Jinja2 template file, of
course,) you have the option of using a builtin base template. If you're
really lazy, you don't even have to put the `{% extends "base.html" %}`
line at the top of your template file--just use the `-e` flag.
(You can also use `--extend-base-template` but if you're too lazy to type
out the directive, you're probably too TL;DR to type the option too.

If you don't specify a `--template` file, the `--extend-base-template`
option won't matter; you'll just get the (rendered, empty) base template, with the options you do or don't ask for.  If you don't specify any input, it will default to an empty JSON object, which is probably what you want, rather than a crash.

### Base template blocks

The base template defines several blocks for your convenience:

* `title`
   Sets the document `title` tag in the `head`.
* `extrahead`
   Allows you to drop style or other tags into the `head`.
* `content`
   Pretty self explanatory.  If you use the `--use-bootstrap` flag with
   the values of `css` or `both`, you'll get a `div.container` around
   this block.
* `extrajs`
   Allows you to drop tags at the end of the `body` tag, where people
   commonly put `script` tags.

This is designed to be a quick and dirty keystroke saver, so don't expect
the world of it.  Feel free to extend and fix it.

Licensed under the MIT License.
