from flask import Flask, request, redirect, render_template, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:password@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'youdamannowdawg'


class Blog(db.Model):
#defines columns or maybe extra tables
#db.Model provides query and such
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(140))
	post = db.Column(db.String(1024))
	
	def __init__(self, title, post):
		self.title=title
		self.post=post
	

	
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
	
		
		if title == "" or post == "":
			#flash('You need to fill out all the fields')
			#go back to the post page with any saved information and display error
			error = "You need to fill out all the fields"
			return render_template('newpost.html', title=title, post=post, error=error)
		
		
		blog = Blog(post=post, title=title)
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
def whole_blog():
#ormobject
	id = request.args.get("id")
	go = False
	if id:
		go = Blog.query.filter_by(id = id)[0]
		
		return render_template('singlepost.html', go = go)
	posts = Blog.query.all()
	#posts = Blog.query.all()[0].post
	#print(posts)
	return render_template('blog.html', posts = posts)





@app.route('/', methods=['POST', 'GET'])
def index():

	return redirect('/blog')


	

	#tasks = Blog.query.filter_by(completed=False).all()
	#completed_tasks = Task.query.filter_by(completed=True).all()
	#return render_template('todos.html',title="Get It Done!", 
		#tasks=tasks, completed_tasks=completed_tasks)


#@app.route('/delete-task', methods=['POST'])



if __name__ == '__main__':
    app.run()