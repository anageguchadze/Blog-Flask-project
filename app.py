from flask import Flask, jsonify, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.secret_key = "your secret key"
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///blog.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

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
    data = request.get_json()
    new_blog = Blog(name=data["name"], subject=data["subject"])
    db.session.add(new_blog)
    db.session.commit()
    return jsonify({"message": "Blog was created!"}), 201

@app.route('/edit/<int:blog_id>', methods=['GET', 'POST'])
def edit_blog(blog_id):
    data = request.get_json()
    blog = Blog.query.get(id)
    if not blog:
        return jsonify({"message": "Blog not found"}), 404
    blog.name = data['name']
    blog.content = data['content']
    db.session.commit()
    return jsonify({"message": "Blog updated successfully"})

@app.route('/delete/<int:blog_id>', methods=['POST'])
def delete_blog(blog_id):
    blog = Blog.query.get(id)
    if not blog:
        return jsonify({"message": "Blog not found"}), 404
    db.session.delete(blog)
    db.session.commit()
    return jsonify({"message": "Blog deleted successfully"})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)