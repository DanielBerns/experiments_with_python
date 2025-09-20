import pdb
import os
import yaml
import subprocess
from datetime import datetime
from pathlib import Path

from flask import Flask, render_template, redirect, url_for, request, flash, Response, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, SelectField, HiddenField
from wtforms.validators import DataRequired, InputRequired, Optional
from werkzeug.security import generate_password_hash, check_password_hash

# --- App Initialization ---
app = Flask(__name__)
# Load secret key from environment variable for security
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'a-secure-default-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../instance/project.db' # SQLite for development
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app) # ORM
login_manager = LoginManager(app) # Authorization
login_manager.login_view = 'login' # Redirect to /login for protected routes

# --- Configuration Loading ---
def load_config():
    """Loads the central YAML configuration file."""
    app_file = Path(__file__)
    config_yaml = app_file.parent / "config.yaml"
    with open(config_yaml, 'r') as f:
        return yaml.safe_load(f)

config = load_config()

# --- Database Models (SQLAlchemy) ---
class User(UserMixin, db.Model):
    """User model for authentication."""
    __tablename__ = 'user' # Explicitly naming table
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password) # Using Werkzeug for hashing

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def create_default_user():
        if not User.query.filter_by(username='admin').first():
            print("Creating default user: admin")
            admin_user = User(username='admin')
            admin_user.set_password('password')
            db.session.add(admin_user)
            db.session.commit()
            print("User 'admin' created with password 'password'.")

class ConfigurationHistory(db.Model):
    """Logs every parameter change for auditing."""
    __tablename__ = 'configuration_history'
    id = db.Column(db.Integer, primary_key=True)
    page_slug = db.Column(db.String(100), nullable=False)
    parameter_name = db.Column(db.String(100), nullable=False)
    value = db.Column(db.Text, nullable=False)
    saved_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('changes', lazy=True))

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

# --- Dynamic Form Generation ---
def create_config_form(page_slug, parameters):
    """Dynamically creates a Flask-WTF form from YAML configuration."""
    class_name = f"{page_slug.replace('-', '_').capitalize()}Form"

    # Base form attributes for save/export logic
    form_attrs = {
        'action': HiddenField('action', default='save'),
        'export_filename': StringField('Export Filename', default=f"{page_slug}-export"),
        'save_submit': SubmitField('Save Configuration'),
        'export_submit': SubmitField('Export to YAML')
    }

    # Dynamically add fields based on parameters
    for param in parameters:
        field_name = param['name']
        field_label = param.get('label', field_name)
        validators = [InputRequired()] if param.get('required', False) else [Optional()]

        field_type = param.get('type', 'text')
        if field_type == 'integer':
            form_attrs[field_name] = IntegerField(field_label, validators=validators, description=param.get('help_text'))
        elif field_type == 'boolean':
            form_attrs[field_name] = BooleanField(field_label, description=param.get('help_text'))
        elif field_type == 'select':
            form_attrs[field_name] = SelectField(field_label, choices=param.get('options', []), validators=validators, description=param.get('help_text'))
        else: # Default to text
            form_attrs[field_name] = StringField(field_label, validators=validators, description=param.get('help_text'))

    return type(class_name, (FlaskForm,), form_attrs)

# --- Authentication Routes ---
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('index'))
        else:
            flash('Invalid username or password.', 'danger')
    return render_template('login.html', form=form, config=config)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

# --- Core Application Routes ---
@app.route('/')
def index():
    # Redirect to the first page defined in the config
    if config['pages']:
        first_page_slug = config['pages'][0]['slug']
        return redirect(url_for('render_page', slug=first_page_slug))
    return "No pages configured in config.yaml", 404

@app.route('/page/<slug>', methods=['GET', 'POST'])
def render_page(slug):
    """Renders a dynamic page based on the slug."""
    page_config = next((p for p in config['pages'] if p['slug'] == slug), None)
    if not page_config:
        return "Page not found", 404

    # Page Protection
    if page_config.get('requires_login', False) and not current_user.is_authenticated:
        return login_manager.unauthorized()

    parameters = page_config.get('parameters', [])
    ConfigForm = create_config_form(slug, parameters)
    form = ConfigForm()

    # --- POST Request Handling (Save or Export) ---
    if form.validate_on_submit():
        action = form.action.data or request.form.get('action')

        # Differentiate between Save and Export action
        if action == 'export':
            # Logic for Configuration Export
            export_data = {}
            for param in parameters:
                field = getattr(form, param['name'])
                export_data[param['name']] = field.data # Create dictionary from form data

            filename = form.export_filename.data.strip().replace(' ', '_')
            if not filename.endswith('.yaml'):
                filename += '.yaml'

            yaml_string = yaml.dump(export_data, default_flow_style=False, indent=2) # Serialize to YAML

            # Generate and return file response
            return Response(
                yaml_string,
                mimetype="text/yaml",
                headers={
                    "Content-Type": "text/yaml; charset=utf-8", #
                    "Content-Disposition": f"attachment; filename=\"{filename}\"" #
                }
            )

        elif action == 'save':
            # Logic for Saving Configuration to DB
            for param in parameters:
                field = getattr(form, param['name'])
                # Save each parameter to the history table
                history_entry = ConfigurationHistory(
                    page_slug=slug,
                    parameter_name=param['name'],
                    value=str(field.data),
                    user_id=current_user.id
                )
                db.session.add(history_entry)
            db.session.commit()
            flash('Configuration saved successfully!', 'success')
            return redirect(url_for('render_page', slug=slug))

    # --- GET Request Handling (Populate Form) ---
    if request.method == 'GET':
        for param in parameters:
            # Find the most recent value for this parameter from the database
            latest_entry = ConfigurationHistory.query.filter_by(
                page_slug=slug,
                parameter_name=param['name']
            ).order_by(ConfigurationHistory.saved_at.desc()).first()

            field = getattr(form, param['name'])
            if latest_entry:
                # Populate from DB
                if param.get('type') == 'boolean':
                    field.data = latest_entry.value.lower() in ['true', '1', 't']
                elif param.get('type') == 'integer' and latest_entry.value.isdigit():
                    field.data = int(latest_entry.value)
                else:
                    field.data = latest_entry.value
            else:
                # Populate from default value in config.yaml
                if 'default' in param:
                    field.data = param['default']

    return render_template('page.html', config=config, page=page_config, form=form)

@app.route('/task/run', methods=['POST'])
@login_required
def run_task():
    """Endpoint to run an asynchronous shell script."""
    data = request.json

    script_path = Path(__file__).parent / data.get('script_path')
    if not script_path or not script_path.exists():
        return jsonify({'status': 'error', 'message': 'Script not found.'}), 404

    try:
        # Run the script in the background
        subprocess.Popen([script_path])
        return jsonify({'status': 'success', 'message': f'Task started: {script_path}'}), 202
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    # Create necessary directories if they don't exist
    os.makedirs('instance', exist_ok=True)
    os.makedirs('app_data/status', exist_ok=True)
    os.makedirs('app_data/reports', exist_ok=True)
    app.run(debug=True)
