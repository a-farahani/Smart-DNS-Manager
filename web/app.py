from flask import Flask, render_template, request, redirect, url_for
from flask_login import login_required
import docker
import os
from auth import auth_bp, init_login  # Import the auth blueprint and login manager

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'default_secret_key')  # Use environment variable or default
MY_VPS_IP = os.getenv('MY_VPS_IP')

# Path to your proxy.conf file
PROXY_CONF_PATH = '/app/dnsmasq/dnsmasq.d/proxy.conf'

# Register the auth blueprint and initialize login
app.register_blueprint(auth_bp)
init_login(app)

# Function to read proxy.conf
def read_proxy_conf():
    with open(PROXY_CONF_PATH, 'r') as file:
        return [line.strip() for line in file.readlines() if line.strip()]

# Function to write to proxy.conf
def write_proxy_conf(entries):
    with open(PROXY_CONF_PATH, 'w') as file:
        for entry in entries:
            file.write(f"{entry}\n")

# Route to display the domains and form
@app.route('/')
@login_required
def index():
    domains = read_proxy_conf()
    return render_template('index.html', domains=domains)

# Route to add a new domain
@app.route('/add', methods=['POST'])
@login_required
def add_domain():
    new_domain = request.form['domain']
    if new_domain:
        entries = read_proxy_conf()
        entries.append(f"address=/.{new_domain}/{MY_VPS_IP}")
        write_proxy_conf(entries)
    return redirect(url_for('index'))

# Route to delete a domain
@app.route('/delete/<domain>')
@login_required
def delete_domain(domain):
    entries = read_proxy_conf()
    entries = [entry for entry in entries if f".{domain}/" not in entry]
    write_proxy_conf(entries)
    return redirect(url_for('index'))

# Function to reload dnsmasq
@app.route('/reload')
@login_required
def reload_dnsmasq():
    client = docker.from_env()
    try:
        container = client.containers.get('dnsmasq')
        container.restart()
        return redirect(url_for('index'))
    except docker.errors.NotFound:
        return "DNSMasq container not found."
    except Exception as e:
        return f"Failed to reload DNSMasq service: {str(e)}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
