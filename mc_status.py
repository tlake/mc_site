"""
A tiny Flask app for Minecraft servers.

Displays server status as well as client configuration and connection
information.
"""

from flask import Flask, render_template


app = Flask(__name__)
app.config.update(
    DEBUG=True,
)


@app.route("/")
def index():
    """Index (and only) page of site."""
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0")
