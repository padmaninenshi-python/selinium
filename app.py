from flask import Flask, render_template, request, send_file
import json
from scraper import scrape_website

app = Flask(__name__)

scraped_data = {}   # Store latest scraped result

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/scrape", methods=["POST"])
def scrape():
    global scraped_data

    url = request.form.get("url")
    scraped_data = scrape_website(url)

    return render_template("result.html", url=url, data=scraped_data)

@app.route("/download")
def download():
    # Save result to JSON file
    with open("scraped.json", "w", encoding="utf-8") as f:
        json.dump(scraped_data, f, indent=4, ensure_ascii=False)

    return send_file("scraped.json", as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
