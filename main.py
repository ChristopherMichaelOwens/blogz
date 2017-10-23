from flask import Flask, request, redirect, render_template, flash, session
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:password@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'youdamannowdawg'

def is_email(string):
    # for our purposes, an email string has an '@' followed by a '.'
    # there is an embedded language called 'regular expression' that would crunch this implementation down
    # to a one-liner, but we'll keep it simple:
    atsign_index = string.find('@')
    atsign_present = atsign_index >= 0
    if not atsign_present:
        return False
    else:
        domain_dot_index = string.find('.', atsign_index)
        domain_dot_present = domain_dot_index >= 0
        return domain_dot_present


class User(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(120), unique=True)
	password = db.Column(db.String(120))
	#unsure about this one
	blogs = db.relationship('Blog', backref='owner')
	
	def __init__(self, username, password):
		self.username = username
		self.password = password
	
	def __repr__(self):
		return '<User %r>' % self.username

class Blog(db.Model):
#defines columns or maybe extra tables
#db.Model provides query and such
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(140))
	post = db.Column(db.String(1024))
	#this is new too. Add property of owner_id
	owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	
	def __init__(self, title, post, owner):
		self.title=title
		self.post=post
		self.owner=owner
		
	def __repr__(self):
		return '<Blog %r>' % self.title

def is_email(string):
    # for our purposes, an email string has an '@' followed by a '.'
    # there is an embedded language called 'regular expression' that would crunch this implementation down
    # to a one-liner, but we'll keep it simple:
    atsign_index = string.find('@')
    atsign_present = atsign_index >= 0
    if not atsign_present:
        return False
    else:
        domain_dot_index = string.find('.', atsign_index)
        domain_dot_present = domain_dot_index >= 0
        return domain_dot_present		
		
@app.route("/signup", methods=['GET', 'POST'])
def signup():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		verify = request.form['verify']
		#if not is_email(email):
		#	flash('zoiks! "' + email + '" does not seem like an email address')
		#	return redirect('/register')
		username_db_count = User.query.filter_by(username=username).count()
		if username_db_count > 0:
			flash('yikes! "' + username + '" is already taken and password reminders are not implemented')
			return redirect('/register')
		if password != verify:
			flash('passwords did not match')
			return redirect('/register')
		user = User(username=username, password=password)
		db.session.add(user)
		db.session.commit()
		session['user'] = user.username
		return redirect("/")
	else:
		return render_template('signup.html')		

@app.route("/login", methods=['GET', 'POST'])
def login():
	if request.method == 'GET':
		return render_template('login.html')
	elif request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		users = User.query.filter_by(username=username)
		if users.count() == 1:
			user = users.first()
			if password == user.password:
				session['user'] = user.username
				flash('welcome back, '+user.username)
				return redirect("/")
		flash('bad username or password')
		return redirect("/login")
		

@app.route("/logout", methods=['POST','GET'])
def logout():
	try:
		del session['user']
	except:
		flash('You cannot log out if you are not logged in.')
	return redirect("/blog")

		
		
	
@app.route('/newpost', methods=['POST','GET'])
def add_post():
#new post?
#assign form fields to variables
#verify form fields
#show errors if errors
#create the object, and put in vars
#put object in to DB
#Commit
#redirect
#else render new blog post template
	if request.method == 'POST':
		title = request.form['title']
		post = request.form['post']
		owner = User.query.filter_by(username=session['user']).first()
		
		if title == "" or post == "":
			#flash('You need to fill out all the fields')
			#go back to the post page with any saved information and display error
			error = "You need to fill out all the fields"
			return render_template('newpost.html', title=title, post=post, error=error)
		
		
		blog = Blog(title, post, owner)
		db.session.add(blog)
		db.session.commit()
		
		id = blog.id
		
	
		
		#id = db.engine.execute("SELECT MAX(id) from blog;").fetchone()[0]
		return redirect("/blog?id=" + str(id))
		#return render_template('blog.html')
	
	else:
		return render_template('newpost.html')
	

#action is the @app.route

@app.route('/blog', methods = ['POST', 'GET'])
def blog():
#ormobject
	id = request.args.get("id")
	userid = request.args.get("user") 
	go = False
	if id:
		go = Blog.query.filter_by(id = id)[0]
		return render_template('singlepost.html', go = go)
	if userid:
		go = Blog.query.filter_by(owner_id = userid).all()
		return render_template('blog.html', posts = go)
	posts = Blog.query.all()
	#posts = Blog.query.all()[0].post
	#print(posts)
	return render_template('blog.html', posts = posts)


@app.before_request
def require_login():
	allowed = ['blog', 'signup', 'login', 'index', 'logout',]
	if request.endpoint not in allowed and 'user' not in session:
		flash('You have to sign up to do that')
		return redirect('/signup')


@app.route('/', methods=['POST', 'GET'])
def index():
	users = User.query.all()
	return render_template("index.html", users = users)
	


	

	#tasks = Blog.query.filter_by(completed=False).all()
	#completed_tasks = Task.query.filter_by(completed=True).all()
	#return render_template('todos.html',title="Get It Done!", 
		#tasks=tasks, completed_tasks=completed_tasks)


#@app.route('/delete-task', methods=['POST'])



if __name__ == '__main__':
    app.run()