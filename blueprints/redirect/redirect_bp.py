from flask import Blueprint, url_for, redirect


redirect_bp = Blueprint('redirect_bp', 
                        __name__)


@redirect_bp.route('/', methods=['GET'])
def index():
    return redirect(url_for('user_bp.index'))