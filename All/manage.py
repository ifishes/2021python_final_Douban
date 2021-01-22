
from flask_script import Manager
from utils.fuctions import create_app
from myapp import db
from flask_migrate import MigrateCommand,Migrate
from myapp.models import User,Data
app=create_app()
manager=Manager(app=app)

migrate = Migrate(app,db)

manager.add_command("db",MigrateCommand)
if __name__=='__main__':
    manager.run()