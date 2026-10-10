
from flask import Flask, request, jsonify, render_template
from urllib.parse import urlparse, parse_qs
import ipaddress

app = Flask(__name__)


def analyze_url(url):
    url = url.strip()

    if not url:
        raise ValueError("Please enter a URL.")

    parsed = urlparse(url)

    if parsed.scheme.lower() not in ("http", "https"):
        raise ValueError("Only HTTP and HTTPS URLs are supported.")

    if not parsed.hostname:
        raise ValueError("Please enter a valid URL with a domain.")

    hostname = parsed.hostname.lower()

    try:
        ipaddress.ip_address(hostname)
        is_ip = True
    except ValueError:
        is_ip = False

    if is_ip:
        domain = hostname
        subdomain = None
    else:
        parts = hostname.split(".")
        domain = ".".join(parts[-2:]) if len(parts) >= 2 else hostname
        subdomain = ".".join(parts[:-2]) or None

    path = parsed.path or "/"
    last_part = path.rstrip("/").split("/")[-1]
    filename = last_part if "." in last_part else None

    return {
        "protocol": parsed.scheme.lower(),
        "domain": domain,
        "subdomain": subdomain,
        "path": path,
        "file_page_name": filename,
        "query_parameters": parse_qs(parsed.query),
        "fragment": parsed.fragment or None
    }


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["GET", "POST"])
def analyze():
    if request.method == "POST":
        data = request.get_json(silent=True) or {}
        url = data.get("url", "")
    else:
        url = request.args.get("url", "")

    try:
        return jsonify(analyze_url(url))
    except ValueError as error:
        return jsonify({"error": str(error)}), 400


if __name__ == "__main__":
    app.run(debug=True)
