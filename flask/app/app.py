
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Configuration

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from flask_admin import Admin
from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView

from flask_security import SQLAlchemyUserDatastore
from flask_security import Security
from flask_security import current_user

from flask import redirect, url_for, request

app = Flask(__name__)
app.config.from_object(Configuration)

db = SQLAlchemy(app)

# механизм миграцией для поддержания корректного состояния бд
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

# Admin
from models import *

# вынесли общую часть классов ниже и наследовали первым аргументом, т.к. эти методы
# переопределяют методы классов из 2-го аргумента
class AdminMixin():
    # для ограничения доступа к админке надо переопределить
    # проверка доступности вьюхи конкретному пользователю
    def is_accessible(self):
        return current_user.has_role('admin')

    # срабатывает, если вьюха не доступна текущему пользователю
    def inaccessible_callback(self, name, **kwargs):
        # redirect перенаправил на стр с логином
        # next указ стр, куда мы попадем когда залогинимся (localhost/admin) - та стр, кот мы запрашивали
        return redirect(url_for('security.login', next=request.url))

# чтоб из админки при создании/изменении какой-нибудь модели(пост, тэг) слаг генерировался сам 
class BaseModelView(ModelView):
    def on_model_change(self, form, model, is_created):
        model.generate_slug()
        return super(BaseModelView, self).on_model_change(form, model, is_created)

# отображение админки
class AdminView(AdminMixin, ModelView):
    pass
    
# чтобы нельзя было из url перейти к админке
class HomeAdminView(AdminMixin, AdminIndexView):
    pass

# опр внешний вид модели пост
class PostAdminView(AdminMixin, BaseModelView):
    form_columns = ['title', 'body', 'tags']

class TagAdminView(AdminMixin, BaseModelView):
    form_columns = ['name', 'posts']

""" admin = Admin(app, 'FlaskApp', url='/', index_view=HomeAdminView(name='Home'))
admin.add_view(PostAdminView(Post, db.session))
admin.add_view(TagAdminView(Tag, db.session)) """

admin = Admin(app)
admin.add_view(ModelView(Post, db.session))
admin.add_view(ModelView(Tag, db.session))

# flask-security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)
