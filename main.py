
import webapp2
import os
import jinja2

from google.appengine.ext import ndb


# Jinja2 Directory Configuration
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

# Models

class User(ndb.Model):
  username = ndb.StringProperty(required = True)
  email = ndb.StringProperty(required = True)
  password = ndb.StringProperty(required = True)
  created_at = ndb.DateTimeProperty(auto_now_add = True)

class Handler(webapp2.RequestHandler):
  def write(self, *a, **kw):
    self.response.out.write(*a, **kw)

  def render_str(self, template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

  def render(self, template, **kw):
    self.write(self.render_str(template, **kw))


class MainHandler(Handler):
  def get(self):
    self.render("main.html")

class LoginHandler(Handler):
  def get(self):
    self.render("login.html")

class SignupHandler(Handler):
  def get(self):
    self.render("signup.html")
 def post(self):
    
  username = self.request.get("username")
    email = self.request.get("email")
    password = self.request.get("password")
    user = User(username = username, email = email, password = password)
    user.put()


app = webapp2.WSGIApplication([
  ('/', MainHandler),
  ('/login', LoginHandler),
  ('/signup', SignupHandler)
])
