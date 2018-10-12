from flask import Blueprint

from app.models import Permission

main = Blueprint('main', __name__)

from app.main import errors, views
from app.models import Permission

@main.app_context_processor
def inject_permission():
    return dict(permission=Permission)