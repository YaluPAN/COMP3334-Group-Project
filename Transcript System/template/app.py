from flask import Flask, render_template, redirect, url_for, request, session
from flask_wtf import FlaskForm
from wtforms import StringField
from flask_wtf.file import FileField, FileAllowed
from werkzeug.utils import secure_filename
from ..myapp import DataBase

app = Flask(__name__)
db=DataBase.Database_operation()

@app.route('/login', methods=['GET', 'POST'])  # 渲染login.html
def login():
    if request.method == 'POST':
        # 检查用户提供的凭据是否正确
        username = request.form['username']
        password = request.form['password']
        res=db.get_account_info(username)
        if username == 'your_username' and password == 'your_password':
            # 设置用户登录状态并重定向到 home 页面
            session['username'] = username
            return redirect(url_for('home'))
        else:
            # 如果凭据不正确，则返回登录页面并显示错误消息
            return render_template('login.html', error='Invalid username or password')
    else:
        # 渲染登录页面
        return render_template('login.html')


@app.route('/')  # 渲染home.html
def home():
    books = [
        {'title': 'Book 1', 'contributor': 'Contributor 1', 'price': '$10'},
        {'title': 'Book 2', 'contributor': 'Contributor 2', 'price': '$20'},
        {'title': 'Book 3', 'contributor': 'Contributor 3', 'price': '$20'},
        # Add more books here
    ]
    account_id = '12345'
    user_name = 'John Doe'
    token_number = 'ABCDE12345'
    purchased_books = ['Book 1', 'Book 2']
    contributed_books = ['Book 3', 'Book 4']

    return render_template('home.html', books=books, account_id=account_id,
                           user_name=user_name,
                           token_number=token_number,
                           purchased_books=purchased_books,
                           contributed_books=contributed_books)


@app.route('/logout')  # 在home.html中，点击“Logout”按钮时，会调用logout()函数，返回login.html
def logout():
    # 从 session 中删除用户信息，并重定向到 login 页面
    session.pop('username', None)
    return redirect(url_for('login'))


# 在home.html中，点击“Make a Contribution”按钮时，会调用make_contribute()函数，进入contribute.html
# @app.route('/make_contribute')
# def make_contribute():
#     return redirect(url_for('contribute'))


class UploadForm(FlaskForm):
    book_title = StringField('Book Title')
    token_price = StringField('Token Price')
    file = FileField('Upload', validators=[FileAllowed(['pdf', 'txt', 'doc'])])


@app.route('/contribute', methods=['GET', 'POST'])  # 渲染contribute.html
def contribute():
    return render_template('contribute.html')


@app.route('/submit', methods=['POST'])
def submit():
    book_title = request.form['bookTitle']
    token_price = request.form['tokenPrice']
    file = request.files['fileInput']
    filename = secure_filename(file.filename)
    # file.save('uploads/' + filename)  # 将文件保存到uploads文件夹中
    # TODO: 将book_title、token_price和文件路径保存到数据库中
    return redirect(url_for('receipt', book_title=book_title, token_price=token_price, filename=filename))


@app.route('/receipt')
def receipt():
    book_title = request.args.get('book_title')
    token_price = request.args.get('token_price')
    return render_template('receipt.html', book_title=book_title, token_price=token_price)


if __name__ == '__main__':
    app.run(debug=True)
