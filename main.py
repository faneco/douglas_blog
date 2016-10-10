
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

    # Handlers

class MainHandler(Handler):
  def get(self):
    user_id = self.request.cookies.get("user_id")
    if user_id:
      self.render("main.html", logado = True)
    else:
      self.render("main.html", logado = False)

class LoginHandler(Handler):
  def get(self):
    self.render("login.html")

  def post(self):
    print "login"
    username = self.request.get("username")
    password = self.request.get("password")
    user = User.query(User.username == username).get()
    if user and user.password == password:
      #vai entrar aqui se o usuario exisitr
      self.response.headers.add_header('Set-Cookie', 'user_id=%s; Path=/' % str(username))
      self.redirect("/")
    else:
      #vai entra aqui se o usuario nao existir
      print("error")
      self.render("login.html", error = True)

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
