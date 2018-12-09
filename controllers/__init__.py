import jinja2


jinja_environment = jinja2.Environment(
        loader=jinja2.FileSystemLoader("templates"),
        extensions=['jinja2.ext.autoescape'],
        autoescape=True)
