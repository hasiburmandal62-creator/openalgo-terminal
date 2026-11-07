from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)

users_db = {"admin": "password123"}
is_logged_in = False

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OpenAlgo - Your Personal Trading Platform</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background-color: #ffffff; color: #24292e; margin: 0; padding: 0; }
        .navbar { display: flex; justify-content: space-between; align-items: center; padding: 20px 40px; border-bottom: 1px solid #eaecef; background: #fff; }
        .logo { font-weight: bold; font-size: 20px; color: #000; display: flex; align-items: center; gap: 8px; }
        .nav-links { display: flex; gap: 20px; font-size: 14px; color: #586069; }
        .btn-black { background: #24292e; color: white; padding: 8px 18px; border-radius: 6px; text-decoration: none; font-size: 14px; font-weight: 500; border: none; cursor: pointer; }
        
        .hero { text-align: center; padding: 80px 20px; background: #fafbfc; border-bottom: 1px solid #eaecef; }
        .hero h1 { font-size: 48px; margin-bottom: 15px; color: #24292e; font-weight: 800; }
        .hero p { font-size: 18px; color: #586069; max-width: 650px; margin: 0 auto 30px auto; line-height: 1.5; }
        
        .auth-container { max-width: 400px; margin: 40px auto; padding: 30px; background: #f6f8fa; border: 1px solid #eaecef; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
        .auth-container h2 { margin-top: 0; font-size: 22px; color: #24292e; text-align: center; margin-bottom: 20px; }
        input { background: #ffffff; color: #24292e; border: 1px solid #d1d5da; padding: 12px; margin: 8px 0 16px 0; border-radius: 6px; width: 100%; font-size: 14px; box-sizing: border-box; }
        
        .terminal-box { max-width: 900px; margin: 40px auto; padding: 30px; background: #0d1117; color: #c9d1d9; border-radius: 8px; font-family: monospace; }
        .terminal-box h2 { color: #58a6ff; margin-top: 0; }
        .stat-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-top: 20px; }
        .stat-card { background: #161b22; border: 1px solid #30363d; padding: 20px; border-radius: 6px; text-align: center; }
        .stat-card h3 { margin: 0; font-size: 14px; color: #8b949e; }
        .stat-card p { font-size: 20px; color: #3fb950; font-weight: bold; margin: 10px 0 0 0; }
        
        .error-msg { color: #d73a49; font-size: 13px; text-align: center; margin-bottom: 10px; }
    </style>
</head>
<body>

    <div class="navbar">
        <div class="logo">⚡ OpenAlgo</div>
        <div class="nav-links">
            <span>Home</span>
            <span>FAQ</span>
            <span>Varsity</span>
            <span>Docs</span>
        </div>
        {% if logged_in %}
            <a href="/logout" class="btn-black" style="background: #d73a49;">Logout</a>
        {% else %}
            <a href="#login" class="btn-black">Login</a>
        {% endif %}
    </div>

    {% if not logged_in %}
    <div class="hero">
        <h1>Your Personal Trading Platform</h1>
        <p>For algo, options and discretionary traders. Open source, community driven, self-hosted across 38+ brokers.</p>
        
        <div class="auth-container" id="login">
            <h2>Sign in to OpenAlgo</h2>
            {% if error %}
                <div class="error-msg">{{ error }}</div>
            {% endif %}
            <form method="POST" action="/login">
                <label style="font-size: 12px; font-weight: bold; display: block; text-align: left;">Username / Email</label>
                <input type="text" name="username" placeholder="Enter username (admin)" required>
                
                <label style="font-size: 12px; font-weight: bold; display: block; text-align: left;">Password</label>
                <input type="password" name="password" placeholder="Enter password (password123)" required>
                
                <button type="submit" class="btn-black" style="width: 100%; padding: 12px;">Login to Terminal</button>
            </form>
        </div>
    </div>
    {% else %}
    <div class="container" style="padding: 20px;">
        <div class="terminal-box">
            <h2>⚡ OpenAlgo Official Trading Dashboard</h2>
            <p>Welcome back, <b>Admin</b>! Connected to self-hosted environment securely.</p>
            
            <div class="stat-grid">
                <div class="stat-card">
                    <h3>Available Balance</h3>
                    <p>₹ 5,43,404.60</p>
                </div>
                <div class="stat-card">
                    <h3>Active Positions</h3>
                    <p>0 (Idle)</p>
                </div>
                <div class="stat-card">
                    <h3>System Status</h3>
                    <p style="color: #3fb950;">● Running</p>
                </div>
            </div>
            
            <div style="margin-top: 30px; text-align: center;">
                <a href="/logout" class="btn-black" style="background: #da3633; padding: 10px 20px;">Disconnect Session</a>
            </div>
        </div>
    </div>
    {% endif %}

</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE, logged_in=is_logged_in)

@app.route('/login', methods=['POST'])
def login():
    global is_logged_in
    username = request.form.get('username')
    password = request.form.get('password')
    
    if username in users_db and users_db[username] == password:
        is_logged_in = True
        return redirect(url_for('home'))
    else:
        return render_template_string(HTML_TEMPLATE, logged_in=False, error="Invalid username or password!")

@app.route('/logout')
def logout():
    global is_logged_in
    is_logged_in = False
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
