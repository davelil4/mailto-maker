from flask import Flask, render_template, request, redirect, url_for, flash
import requests
import re

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flash messages

def generate_mailto_link(email: str, subject: str, body: str, cc: str, bcc: str) -> str:
    link = f"mailto:{email}"
    params = []
    if subject:
        params.append(f"subject={requests.utils.quote(subject)}")
    if body:
        params.append(f"body={requests.utils.quote(body)}")
    if cc:
        params.append(f"cc={requests.utils.quote(cc)}")
    if bcc:
        params.append(f"bcc={requests.utils.quote(bcc)}")
    
    if params:
        link += "?" + "&".join(params)
    
    return link

def shorten_url(url: str, alias: str, auth_key: str) -> str:
    api_url = "https://api.tinyurl.com/create"
    headers = {
        'Authorization': f'Bearer {auth_key}',
        'Content-Type': 'application/json'
    }
    data = {
        "url": url,
        "domain": "tinyurl.com"
    }
    if alias:
        data["alias"] = alias

    response = requests.post(api_url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json().get('data', {}).get('tiny_url')
    else:
        raise Exception(f"Failed to shorten URL: {response.json().get('errors')}")

def update_url(url: str, alias: str, auth_key: str) -> str:
    api_url = f"https://api.tinyurl.com/update/{alias}"
    headers = {
        'Authorization': f'Bearer {auth_key}',
        'Content-Type': 'application/json'
    }
    data = {
        "url": url,
        "domain": "tinyurl.com"
    }

    response = requests.put(api_url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json().get('data', {}).get('tiny_url')
    else:
        raise Exception(f"Failed to update URL: {response.json().get('errors')}")

def is_valid_email(email: str) -> bool:
    pattern = r"[^@]+@[^@]+\.[^@]+"
    return re.match(pattern, email) is not None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email = request.form['email']
        subject = request.form['subject']
        body = request.form['body']
        cc = request.form['cc']
        bcc = request.form['bcc']
        alias = request.form['alias']
        auth_key = request.form['auth_key']
        action = request.form['action']

        # Validate emails
        emails = [e.strip() for e in email.split(',')]
        ccs = [e.strip() for e in cc.split(',')] if cc else []
        bccs = [e.strip() for e in bcc.split(',')] if bcc else []

        all_emails = emails + ccs + bccs
        for addr in all_emails:
            if not is_valid_email(addr):
                flash('Invalid email address: ' + addr, 'error')
                return render_template('index.html', email=email, subject=subject, body=body, cc=cc, bcc=bcc, alias=alias, auth_key=auth_key)
        
        if not auth_key:
            flash('Authorization key is required', 'error')
            return render_template('index.html', email=email, subject=subject, body=body, cc=cc, bcc=bcc, alias=alias, auth_key=auth_key)
        
        try:
            mailto_link = generate_mailto_link(','.join(emails), subject, body, ','.join(ccs), ','.join(bccs))
            if action == 'shorten':
                short_link = shorten_url(mailto_link, alias, auth_key)
            elif action == 'update':
                short_link = update_url(mailto_link, alias, auth_key)
            else:
                flash('Invalid action', 'error')
                return render_template('index.html', email=email, subject=subject, body=body, cc=cc, bcc=bcc, alias=alias, auth_key=auth_key)

            return render_template('index.html', short_link=short_link, email=email, subject=subject, body=body, cc=cc, bcc=bcc, alias=alias, auth_key=auth_key)
        except Exception as e:
            flash(f"Error: {str(e)}", 'error')
            return render_template('index.html', email=email, subject=subject, body=body, cc=cc, bcc=bcc, alias=alias, auth_key=auth_key)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
