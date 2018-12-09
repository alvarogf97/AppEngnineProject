import jinja2


def init_jinja_render():
    jinja_environment = jinja2.Environment(
        loader=jinja2.FileSystemLoader("../templates"),
        extensions=['jinja2.ext.autoescape'],
        autoescape=True)
    return jinja_environment
