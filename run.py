from app import app, db
from app.models import User, Product

if __name__ == '__main__':
    app.run()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Product': Product}