from flask import Flask, render_template, request, redirect, url_for, flash
import threading
from api import ApiClient
from aws_handler import AWSClient

app = Flask(__name__)
app.secret_key = 'dev-secret-key'  # Required for flash messages

# Initialize clients
api = ApiClient()
aws = AWSClient()

def save_async(articles, topic):
    """Background task to save articles without blocking the UI."""
    # Create a new client for thread safety
    local_aws = AWSClient()
    count = 0
    for article in articles:
        if local_aws.save_article(article, topic):
            count += 1
    print(f"Background save completed: {count} articles.")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        country_name = request.form.get('country')
        topic = request.form.get('topic')
        language = request.form.get('language', 'en')

        if not country_name or not topic:
            flash("Please enter both country and topic.", "danger")
            return redirect(url_for('index'))

        # 1. Fetch Country Details
        country_data = api.get_country_details(country_name)
        if not country_data:
            flash(f"Could not find country: {country_name}", "danger")
            return redirect(url_for('index'))

        country_code = country_data.get('cca2')

        # 2. Fetch News
        articles = api.get_news(country_code, topic, language)
        if not articles:
            flash("No news found for this criteria.", "warning")
            return redirect(url_for('index'))

        # 3. Save to AWS
        # Run in background to speed up response
        thread = threading.Thread(target=save_async, args=(articles, topic))
        thread.start()
        
        flash(f"Success! Found {len(articles)} articles. Saving to AWS in background...", "success")
        
        return render_template('results.html', articles=articles, country=country_data, topic=topic)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)