from flask import Flask, render_template, request, redirect, url_for, session
import requests
from requests.exceptions import RequestException
import favicon
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secure random secret key

def fetch_favicon(url):
    try:
        icons = favicon.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'})
        if icons:
            return icons[0].url
    except RequestException as e:
        print(f"Error fetching favicon: {e}")
    return "/static/default_logo.png"  # Fallback logo

@app.route('/')
def index():
    if 'websites' not in session:
        session['websites'] = []
    return render_template('index.html', websites=session['websites'])

@app.route('/add', methods=['GET', 'POST'])
def add_website():
    if request.method == 'POST':
        website_name = request.form['name']
        website_url = request.form['url']
        website_logo = fetch_favicon(website_url)
        websites = session.get('websites', [])
        websites.append({'name': website_name, 'url': website_url, 'logo': website_logo, 'favorite': False})
        session['websites'] = websites
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/delete/<int:website_id>')
def delete_website(website_id):
    websites = session.get('websites', [])
    if 0 <= website_id < len(websites):
        websites.pop(website_id)
        session['websites'] = websites
    return redirect(url_for('index'))

@app.route('/favorite/<int:website_id>')
def favorite_website(website_id):
    websites = session.get('websites', [])
    if 0 <= website_id < len(websites):
        # Toggle the favorite status
        websites[website_id]['favorite'] = not websites[website_id]['favorite']
        # Move the website to the top of the list if it is now a favorite
        if websites[website_id]['favorite']:
            websites.insert(0, websites.pop(website_id))
        else:
            # If unfavorited, keep the order (or optionally move it to the bottom)
            pass
        session['websites'] = websites
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
