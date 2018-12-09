import webapp2
from controllers import jinja_environment


class HelloWorldHandler(webapp2.RequestHandler):
    def get(self):
        template_values = {"msg":"hello world :)"}
        template = jinja_environment.get_template('helloWorld.html')
        self.response.write(template.render(template_values))