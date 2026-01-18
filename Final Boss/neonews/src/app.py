from flask import Flask, render_template, request, redirect, url_for, flash
import threading
import logging
from api import ApiClient
from aws_handler import AWSClient

app = Flask(__name__)
app.secret_key = 'dev-secret-key'  # Required for flash messages

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize clients
api = ApiClient()
aws = AWSClient()

def save_async(articles, topic):
    """Background task to save articles without blocking the UI."""
    logger.info(f"Starting background save for topic: {topic} with {len(articles)} articles.")
    # Create a new client for thread safety
    local_aws = AWSClient()
    count = 0
    for article in articles:
        if local_aws.save_article(article, topic):
            count += 1
    logger.info(f"Background save completed: {count} articles saved successfully.")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        country_name = request.form.get('country')
        topic = request.form.get('topic')
        language = request.form.get('language', 'en')
        
        logger.info(f"Received POST request: Country='{country_name}', Topic='{topic}', Language='{language}'")

        if not country_name or not topic:
            logger.warning("Validation failed: Missing country or topic.")
            flash("Please enter both country and topic.", "danger")
            return redirect(url_for('index'))

        # 1. Fetch Country Details
        logger.info(f"Fetching details for country: {country_name}")
        country_data = api.get_country_details(country_name)
        if not country_data:
            logger.warning(f"Country not found: {country_name}")
            flash(f"Could not find country: {country_name}", "danger")
            return redirect(url_for('index'))

        country_code = country_data.get('cca2')

        # 2. Fetch News
        logger.info(f"Fetching news for country code: {country_code}, topic: {topic}")
        articles = api.get_news(country_code, topic, language)
        if not articles:
            logger.warning("No news articles found for the given criteria.")
            flash("No news found for this criteria.", "warning")
            return redirect(url_for('index'))

        # 3. Save to AWS
        # Run in background to speed up response
        logger.info("Spawning background thread for AWS persistence.")
        thread = threading.Thread(target=save_async, args=(articles, topic))
        thread.start()
        
        flash(f"Success! Found {len(articles)} articles. Saving to AWS in background...", "success")
        
        return render_template('results.html', articles=articles, country=country_data, topic=topic)

    return render_template('index.html')

@app.route('/clear-s3', methods=['POST'])
def clear_s3():
    aws.clear_s3_bucket()
    flash("S3 bucket has been cleared.", "success")
    return redirect(url_for('index'))

@app.route('/clear-dynamodb', methods=['POST'])
def clear_dynamodb():
    aws.clear_dynamodb_table()
    flash("DynamoDB table has been cleared.", "success")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)