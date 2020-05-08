from flask import Flask, render_template
from string import digits, ascii_lowercase
from random import sample
from mars.views.authenticate import login_check, authenticate
from mars.views.index import index
from mars.views.poc_scanner import poc_scanner
from mars.views.asset_management import asset_management
from mars.views.plugin_management import plugin_management
from mars.views.settings import settings
from mars.views.dashboard import dashboard
from mars.views.port_scanner import port_scanner
from mars.views.subdomain_brute import subdomain_brute
from mars.views.vul_scanner import vul_scanner
from mars.views.auth_tester import auth_tester
from mars.views.customer import customer



app = Flask(__name__)
app.config['SECRET_KEY'] = ''.join(sample(digits + ascii_lowercase, 10))

app.register_blueprint(authenticate)
app.register_blueprint(index)
app.register_blueprint(poc_scanner)
app.register_blueprint(asset_management)
app.register_blueprint(plugin_management)
app.register_blueprint(settings)
app.register_blueprint(dashboard)
app.register_blueprint(port_scanner)
app.register_blueprint(subdomain_brute)
app.register_blueprint(vul_scanner)
app.register_blueprint(auth_tester)
app.register_blueprint(customer)


@app.errorhandler(404)
@login_check
def page_not_fount(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
@login_check
def internal_server_error(e):
    return render_template('500.html'), 500
