from flask import Flask, jsonify, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api, Resource, fields

app = Flask(__name__)

# Flask App Configuration
app.secret_key = "your secret key"
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///blog.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize the database
db = SQLAlchemy(app)

# Flask-RESTX Setup for Swagger
api = Api(app, version='1.0', title='Blog API', description='A simple blog API')
ns = api.namespace('blogs', description='Blog operations')

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Swagger Model for Blog
blog_model = api.model('Blog', {
    'id': fields.Integer(readonly=True, description='The unique identifier of a blog'),
    'title': fields.String(required=True, description='The title of the blog'),
    'content': fields.String(required=True, description='The content of the blog'),
    'author_id': fields.Integer(required=True, description='The ID of the author'),
})

# Routes

@app.route('/')
def home():
    if 'username' in session:
        blogs = Blog.query.all()
        return render_template("blogs.html", blogs=blogs)
    return "<a href='/login'>Login</a> or <a href='/register'>Register</a>"

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        if User.query.filter_by(username=username).first():
            return "Username already exists"

        hashed_password = generate_password_hash(password, method="pbkdf2:sha256")

        new_user = User(username=username, password=hashed_password)

        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template("register.html")

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['username'] = user.username
            session['user_id'] = user.id
            return redirect(url_for('home'))
        else:
            return "Invalid username or password"

    return render_template("login.html")

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('user_id', None)
    return redirect(url_for('home'))

@app.route('/create', methods=['GET', 'POST'])
def create_blog():
    if request.method == "POST":
        title = request.form['title']
        content = request.form['content']
        author_id = session.get('user_id')  # Get the logged-in user's ID

        if not author_id:
            return redirect(url_for('login'))  # Ensure user is logged in

        new_blog = Blog(title=title, content=content, author_id=author_id)
        db.session.add(new_blog)
        db.session.commit()
        return redirect(url_for('home'))

    return render_template("create_blog.html")


@app.route('/edit/<int:blog_id>', methods=['GET', 'POST'])
def edit_blog(blog_id):
    blog = Blog.query.get(blog_id)
    if not blog:
        return jsonify({"message": "Blog not found"}), 404

    if request.method == "POST":
        if blog.author_id != session.get('user_id'):
            return jsonify({"message": "Unauthorized"}), 403  # Ensure only the author can edit

        blog.title = request.form['title']
        blog.content = request.form['content']
        db.session.commit()
        return redirect(url_for('home'))

    return render_template("edit_blog.html", blog=blog)


@app.route('/delete/<int:blog_id>', methods=['POST'])
def delete_blog(blog_id):
    blog = Blog.query.get(blog_id)
    if not blog:
        return jsonify({"message": "Blog not found"}), 404

    if blog.author_id != session.get('user_id'):
        return jsonify({"message": "Unauthorized"}), 403  # Ensure only the author can delete

    db.session.delete(blog)
    db.session.commit()
    return redirect(url_for('home'))


# API Routes for Blog Management with Swagger Documentation

@ns.route('/')
class BlogList(Resource):
    def get(self):
        """Get a list of all blogs"""
        blogs = Blog.query.all()
        return jsonify([{
            'id': blog.id,
            'title': blog.title,
            'content': blog.content,
            'author_id': blog.author_id
        } for blog in blogs])

    @api.expect(blog_model)
    def post(self):
        """Create a new blog"""
        data = api.payload
        new_blog = Blog(
            title=data['title'],
            content=data['content'],
            author_id=data['author_id']
        )
        db.session.add(new_blog)
        db.session.commit()
        return {'message': 'Blog created successfully'}, 201

@ns.route('/<int:id>')
@api.response(404, 'Blog not found')
@api.param('id', 'The blog identifier')
class BlogResource(Resource):
    def get(self, id):
        """Get a single blog by its ID"""
        blog = Blog.query.get(id)
        if not blog:
            api.abort(404, "Blog not found")
        return {
            'id': blog.id,
            'title': blog.title,
            'content': blog.content,
            'author_id': blog.author_id
        }

    @api.expect(blog_model)
    def put(self, id):
        """Update a blog"""
        blog = Blog.query.get(id)
        if not blog:
            api.abort(404, "Blog not found")
        data = api.payload
        blog.title = data['title']
        blog.content = data['content']
        db.session.commit()
        return {'message': 'Blog updated successfully'}

    def delete(self, id):
        """Delete a blog"""
        blog = Blog.query.get(id)
        if not blog:
            api.abort(404, "Blog not found")
        db.session.delete(blog)
        db.session.commit()
        return {'message': 'Blog deleted successfully'}

# Initialize the app
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create tables in the database
    app.run(debug=True)
