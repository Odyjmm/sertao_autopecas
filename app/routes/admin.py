from flask import Blueprint, render_template

admin = Blueprint('admin', __name__)

@admin.route('/admin')
def admin_home():
    return "<h1>Painel Admin</h1>"