from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)

users_db = {"admin": "password123"}
is_logged_in = False
active_broker = None

# ব্রোকার লিস্ট এবং কনফিগারেশন স্টেট
brokers_db = {
    "Fyers": {"configured": False, "client_id": "", "secret": ""},
    "5 Paisa": {"configured": False, "client_id": "", "secret": ""},
    "Angel One": {"configured": False, "client_id": "", "secret": ""},
    "Alice Blue": {"configured": False, "client_id": "", "secret": ""},
    "Dhan": {"configured": False, "client_id": "", "secret": ""},
    "Delta Exchange": {"configured": False, "client_id": "", "secret": ""}
}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OpenAlgo - Trading Terminal</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background-color: #f8f9fa; color: #24292e; margin: 0; padding: 0; }
        .navbar { display: flex; justify-content: space-between; align-items: center; padding: 14px 30px; background: #fff; border-bottom: 1px solid #eaecef; }
        .logo { font-weight: bold; font-size: 18px; color: #000; display: flex; align-items: center; gap: 8px; }
        .nav-links { display: flex; gap: 20px; font-size: 13px; color: #586069; align-items: center; }
        .nav-links a { text-decoration: none; color: #24292e; font-weight: 500; }
        .nav-links a:hover { color: #0366d6; }
        
        .container { max-width: 1100px; margin: 30px auto; padding: 0 15px; }
        h2 { font-size: 22px; margin-bottom: 5px; }
        .sub-text { font-size: 13px; color: #586069; margin-bottom: 25px; }
        
        .broker-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 20px; }
        .broker-card { background: #fff; border: 1px solid #eaecef; border-radius: 8px; padding: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.02); }
        .broker-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }
        .broker-name { font-weight: bold; font-size: 16px; color: #24292e; }
        .badge-not { font-size: 11px; color: #e36209; background: #fff5eb; padding: 3px 8px; border-radius: 10px; font-weight: 500; }
        .badge-conf { font-size: 11px; color: #28a745; background: #dafbe1; padding: 3px 8px; border-radius: 10px; font-weight: 500; }
        .exchanges { font-size: 11px; color: #6a737d; margin-bottom: 15px; }
        
        .btn-config { display: block; width: 100%; text-align: center; background: #fafbfc; border: 1px solid #d1d5da; color: #24292e; padding: 8px; border-radius: 6px; text-decoration: none; font-size: 13px; font-weight: 500; box-sizing: border-box; }
        .btn-config:hover { background: #f3f4f6; }
        .btn-login { background: #24292e; color: #fff; border: none; }
        .btn-login:hover { background: #2c3238; }

        .form-card { background: #fff; border: 1px solid #eaecef; border-radius: 8px; padding: 30px; max-width: 600px; margin: 20px auto; }
        input { background: #fff; color: #24292e; border: 1px solid #d1d5da; padding: 10px; margin: 8px 0 16px 0; border-radius: 6px; width: 100%; font-size: 13px; box-sizing: border-box; }
        label { font-size: 12px; font-weight: bold; color: #24292e; }
        
        .auth-container { max-width: 380px; margin: 60px auto; padding: 30px; background: #fff; border: 1px solid #eaecef; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
        .error-msg { color: #d73a49; font-size: 12px; text-align: center; margin-bottom: 10px; }

        /* Dashboard Styles */
        .dash-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-top: 20px; }
        .dash-card { background: #fff; border: 1px solid #eaecef; padding: 20px; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.02); }
        .dash-card h3 { margin: 0; font-size: 13px; color: #586069; font-weight: 500; }
        .dash-card p { font-size: 20px; color: #24292e; font-weight: bold; margin: 8px 0 0 0; }
        
        .quick-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 15px; margin-top: 30px; }
        .quick-box { background: #fff; border: 1px solid #eaecef; padding: 18px; border-radius: 8px; text-decoration: none; color: inherit; display: block; }
        .quick-box:hover { border-color: #0366d6; }
        .quick-box h4 { margin: 0 0 5px 0; font-size: 14px; color: #0366d6; }
        .quick-box p { margin: 0; font-size: 12px; color: #586069; }
    </style>
</head>
<body>

    <div class="navbar">
        <div class="logo">⚡ OpenAlgo</div>
        {% if logged_in %}
        <div class="nav-links">
            <a href="/dashboard">Dashboard</a>
            <a href="/brokers">Brokers</a>
            <span>Orderbook</span>
            <span>Tradebook</span>
            <span>Positions</span>
            <span style="color: #28a745; font-weight: bold;">● {{ active_broker if active_broker else "No Broker" }}</span>
            <a href="/logout" style="color: #d73a49;">Sign out</a>
        </div>
        {% endif %}
    </div>

    {% if not logged_in %}
    <div class="auth-container">
        <h2 style="text-align: center; margin-top:0;">Sign in to OpenAlgo</h2>
        {% if error %}
            <div class="error-msg">{{ error }}</div>
        {% endif %}
        <form method="POST" action="/login">
            <label>Username / Email</label>
            <input type="text" name="username" placeholder="admin" required>
            <label>Password</label>
            <input type="password" name="password" placeholder="password123" required>
            <button type="submit" class="btn-config btn-login" style="width: 100%; padding: 10px; cursor: pointer;">Login</button>
        </form>
    </div>

    {% elif view == 'dashboard' %}
    <div class="container">
        <h2>Trading Dashboard</h2>
        <p class="sub-text">Overview of your trading account and market positions via <b>{{ active_broker }}</b>.</p>
        
        <div class="dash-grid">
            <div class="dash-card">
                <h3>Available Balance</h3>
                <p style="color: #28a745;">₹ 5,43,404.60</p>
            </div>
            <div class="dash-card">
                <h3>Collateral</h3>
                <p>₹ 0.00</p>
            </div>
            <div class="dash-card">
                <h3>Unrealized P&L</h3>
                <p>₹ 0.00</p>
            </div>
            <div class="dash-card">
                <h3>Realised P&L</h3>
                <p>₹ 0.00</p>
            </div>
            <div class="dash-card">
                <h3>Utilised Margin</h3>
                <p>₹ 0.00</p>
            </div>
        </div>

        <h3 style="margin-top: 35px;">Quick Access</h3>
        <div class="quick-grid">
            <div class="quick-box">
                <h4>OpenAlgo Symbols</h4>
                <p>Universal symbology across brokers</p>
            </div>
            <div class="quick-box">
                <h4>Documentation</h4>
                <p>Tutorials, API docs & features</p>
            </div>
            <div class="quick-box">
                <h4>Live Logs</h4>
                <p>Real-time trading activity logs</p>
            </div>
            <div class="quick-box">
                <h4>P&L Tracker</h4>
                <p>Live intraday MTM tracker</p>
            </div>
        </div>
    </div>

    {% elif view == 'config' %}
    <div class="container">
        <div class="form-card">
            <a href="/brokers" style="font-size: 12px; color: #0366d6; text-decoration: none;">← Back to Select Broker</a>
            <h2 style="margin-top: 15px;">Configure {{ broker_name }}</h2>
            <p class="sub-text">Save your API keys securely for {{ broker_name }}.</p>
            
            <form method="POST" action="/save_broker/{{ broker_name }}">
                <label>Client ID and API Key / App Key</label>
                <input type="text" name="client_id" value="{{ details.client_id }}" placeholder="Enter API Key" required>
                
                <label>API Secret</label>
                <input type="password" name="secret" value="{{ details.secret }}" placeholder="Enter API Secret" required>
                
                <label>Redirect URL</label>
                <input type="text" value="https://openalgo-terminal.onrender.com/callback" readonly style="background: #f6f8fa; color: #586069;">
                
                <button type="submit" class="btn-config btn-login" style="padding: 10px; cursor: pointer; margin-top: 10px;">Save Keys</button>
            </form>
        </div>
    </div>

    {% else %}
    <div class="container">
        <h2>Select Broker</h2>
        <div class="sub-text">Save keys for as many brokers as you like; one broker is logged in at a time.</div>
        
        <div class="broker-grid">
            {% for b_name, info in brokers.items() %}
            <div class="broker-card">
                <div class="broker-header">
                    <span class="broker-name">{{ b_name }}</span>
                    {% if info.configured %}
                        <span class="badge-conf">Configured</span>
                    {% else %}
                        <span class="badge-not">Not Configured</span>
                    {% endif %}
                </div>
                <div class="exchanges">
                    {% if b_name == 'Delta Exchange' %}
                        Exchanges: CRYPTO DERIVATIVES
                    {% else %}
                        Exchanges: NSE, BSE, NFO, BFO, CDS, MCX
                    {% endif %}
                </div>
                
                {% if info.configured %}
                    <a href="/connect/{{ b_name }}" class="btn-config btn-login">Login with {{ b_name }}</a>
                    <a href="/configure/{{ b_name }}" style="font-size: 11px; color: #0366d6; text-decoration: none; display: block; text-align: center; margin-top: 8px;">Edit keys</a>
                {% else %}
                    <a href="/configure/{{ b_name }}" class="btn-config">Configure</a>
                {% endif %}
            </div>
            {% endfor %}
        </div>
    </div>
    {% endif %}

</body>
</html>
"""

@app.route('/')
def home():
    if not is_logged_in:
        return render_template_string(HTML_TEMPLATE, logged_in=False)
    return redirect(url_for('brokers_page'))

@app.route('/login', methods=['POST'])
def login():
    global is_logged_in
    username = request.form.get('username')
    password = request.form.get('password')
    if username in users_db and users_db[username] == password:
        is_logged_in = True
        return redirect(url_for('brokers_page'))
    return render_template_string(HTML_TEMPLATE, logged_in=False, error="Invalid username or password!")

@app.route('/brokers')
def brokers_page():
    if not is_logged_in:
        return redirect(url_for('home'))
    return render_template_string(HTML_TEMPLATE, logged_in=True, view='list', brokers=brokers_db, active_broker=active_broker)

@app.route('/configure/<b_name>')
def configure_broker(b_name):
    if not is_logged_in:
        return redirect(url_for('home'))
    return render_template_string(HTML_TEMPLATE, logged_in=True, view='config', broker_name=b_name, details=brokers_db[b_name], active_broker=active_broker)

@app.route('/save_broker/<b_name>', methods=['POST'])
def save_broker(b_name):
    if not is_logged_in:
        return redirect(url_for('home'))
    brokers_db[b_name]['client_id'] = request.form.get('client_id')
    brokers_db[b_name]['secret'] = request.form.get('secret')
    brokers_db[b_name]['configured'] = True
    return redirect(url_for('brokers_page'))

@app.route('/connect/<b_name>')
def connect_broker(b_name):
    global active_broker
    if not is_logged_in:
        return redirect(url_for('home'))
    active_broker = b_name
    return redirect(url_for('dashboard_page'))

@app.route('/dashboard')
def dashboard_page():
    if not is_logged_in:
        return redirect(url_for('home'))
    return render_template_string(HTML_TEMPLATE, logged_in=True, view='dashboard', brokers=brokers_db, active_broker=active_broker)

@app.route('/logout')
def logout():
    global is_logged_in, active_broker
    is_logged_in = False
    active_broker = None
    return redirect(url_for('home'))

if __name__ == 'main':
    app.run(host='0.0.0.0', port=5000)
