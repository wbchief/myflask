from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_script import Shell

from app import create_app, db
from app.models import User, Role, Post

app = create_app('testing')
manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role, Post=Post)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()