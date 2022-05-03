from flask import Blueprint


micro_scheme_bp = Blueprint('micro_scheme_bp', __name__)

@micro_scheme_bp.route('/configure_scheme', methods=['GET'])
def configure_scheme():
    return {'delay':2000},200, {"Access-Control-Allow-Origin": "*"}