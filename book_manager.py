from flask import Flask, render_template, flash, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from wtforms.validators import DataRequired
from wtforms import StringField, SubmitField
from flask_wtf import FlaskForm

app = Flask(__name__)
# 数据库的配置
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@127.0.0.1/flask_book'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'luhang'

# WTF
class AuthorForm(FlaskForm):
    author = StringField('author', validators=[DataRequired()])
    book = StringField('bookname', validators=[DataRequired()])
    submmit = SubmitField('comfirm')

# 创建数据库对象
db = SQLAlchemy(app)

class Author(db.Model):
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16), unique=True)
    #关系引用
    books = db.relationship('Book',backref='author')

    def __repr__(self):
        return 'author: %s' % self.name

class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=False)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'))

    def __repr__(self):
        return 'Book %s' % self.name
'''
1.配置数据库
2.添加书籍和作者模型
3.添加数据
4.使用模板显示数据库的查询数据
5.使用WTF表单
6.实现相关的增删操作

'''
# 作者的删除
@app.route('/delete_author/<author_id>')
def delete_author(author_id):
    author = Author.query.get(author_id)
    if author:
        try:
            Book.query.filter_by(author_id=author.id).delete()
            db.session.delete(author)
            db.session.commit()
        except Exception as e:
            print(e)
            flash('删除作者失败')
            db.session.rollback()
    else:
        flash('没有该作者，删除失败')
    return redirect(url_for('index'))

# 书籍的删除
@app.route('/delete_book/<book_id>')
def delete_book(book_id):
    # 查看是否有改书籍
    book = Book.query.get(book_id)
    if book:
        try:
            db.session.delete(book)
            db.session.commit()
        except Exception as e:
            print(e)
            flash('删除书籍失败')
            db.session.rollback()
    else:
        flash('没有该书籍，请输入正确的书籍')
    return redirect(url_for('index'))

@app.route('/', methods=['GET', 'POST'])
def index():
    '''
    1. 调用WTF的函数实现验证
    2. 验证通过则获取数据
    3. 判断作者是否存在
    4. 如果作者存在，判断书籍是否存在，没有重复书籍则添加书籍，否则提升错误
    5. 如果作者不存在，添加作者和书籍
    6. 验证不通过就提示错误
    '''
    author_form = AuthorForm()

    # 1. 调用WTF的函数实现验证
    if author_form.validate_on_submit():
        # 2. 验证通过则获取数据
        author_name = author_form.author.data
        book_name = author_form.book.data

        # 3. 判断作者是否存在
        author = Author.query.filter_by(name=author_name).first()
        # 4. 如果作者存在，
        if author:
            # 判断书籍是否存在
            book = Book.query.filter_by(name=book_name).first()
            if book:
                flash('The book is already exitsts!')
            else:
                # 没有重复书籍则添加书籍
                try:
                    newBook = Book(name=book_name, author_id=author.id)
                    db.session.add(newBook)
                    db.session.commit()
                except Exception as e:
                    print(e)
                    flash('Add book error')
                    db.session.rollback()
        else:
            # 5. 如果作者不存在，添加作者和书籍
            try:
                newAuthor = Author(name=author_name)
                db.session.add(newAuthor)
                db.session.commit()

                new_book = Book(name=book_name, author_id=newAuthor.id)
                db.session.add(new_book)
                db.session.commit()
            except Exception as e:
                print(e)
                flash('Add author and book error')
                db.session.rollback()
    else:
        # 6. 验证不通过就提示错误
        if request.method == 'POST':
            flash('error')

    authors = Author.query.all()
    return render_template('books.html', authors=authors, form=author_form)

if __name__ == '__main__':
    db.drop_all()
    db.create_all()

    # 生成数据
    au1 = Author(name='路航')
    au2 = Author(name='姚军')
    au3 = Author(name='秦好')
    # 添加到session回话
    db.session.add_all([au1, au2, au3])
    # 提交会话
    db.session.commit()

    bk1 = Book(name='隔壁王嫂',author_id=au1.id)
    bk2 = Book(name='HipHop很low',author_id=au1.id)
    bk3 = Book(name='destory my life',author_id=au1.id)
    bk4 = Book(name='秦氏有几集',author_id=au3.id)
    bk5 = Book(name='My big House',author_id=au2.id)
    db.session.add_all([bk1,bk2,bk3,bk4,bk5])
    db.session.commit()

    app.run()
