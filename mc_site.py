"""
A tiny Flask app for Minecraft servers.

Displays server status as well as client configuration and connection
information.
"""

from flask import Flask, render_template, request, jsonify
from flask.ext.misaka import Misaka
from flask.ext.sqlalchemy import SQLAlchemy

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from mcstatus import MinecraftServer

import os


################################
# APP SETTINGS
################################

DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_CRED = DB_USER + ":" + DB_PASS
DB_NAME = "mc_site_db"

app = Flask(__name__)
Misaka(app)
app.config.update(
    DEBUG=True,
    SECRET_KEY="man, who knows?",
    SQLALCHEMY_DATABASE_URI="postgresql://" + DB_CRED + "@localhost/" + DB_NAME
)


################################
# DATABASE SETTINGS & MODELS
################################

db = SQLAlchemy(app)


class Server(db.Model):
    """Server model."""

    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(128))
    port = db.Column(db.Integer)
    modpack_version = db.Column(db.String(64))
    client_config = db.Column(db.Text)
    created = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
    )


class Message(db.Model):
    """Model for message to be displayed on the site."""

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256))
    display = db.Column(db.Boolean)
    body = db.Column(db.Text)
    created = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
    )


db.create_all()
db.session.commit()


################################
# ADMIN SETTINGS & VIEWS
################################

admin = Admin(app)
admin.add_view(ModelView(Server, db.session))
admin.add_view(ModelView(Message, db.session))


################################
# APP VIEWS
################################

@app.route("/")
def index():
    """Index (and only) page of site."""
    render_obj = []
    message_objects = Message.query.filter_by(display=True).all()
    server_objects = Server.query.all()

    for server in server_objects:
        address = server.address
        port = server.port
        conn = MinecraftServer(address, port)

        try:
            conn.ping()
        # except ConnectionRefusedError:
        # Commented out because for some reason on the production server,
        # attempting to catch this error causes the site to break and display
        # 'Internal Server Error'. Logs from such events say that
        # 'ConnectionRefusedError' is undefined, although there seem to be no
        # issues when testing locally.
        except:
            render_obj.append({
                "address": address,
                "port": port,
                "modpack_version": server.modpack_version,
                "client_config": server.client_config,
                "status": "Offline",
            })
        else:
            add_to_render = {}
            q = conn.query()
            motd = q.motd
            players = {
                "max": q.players.max,
                "online": q.players.online,
                "names": q.players.names,
            }
            jar_version = q.software.version

            add_to_render.update({
                "address": address,
                "port": port,
                "modpack_version": server.modpack_version,
                "client_config": server.client_config,
                "status": "Online",
                "motd": motd,
                "players": players,
                "jar_version": jar_version,
            })

            render_obj.append(add_to_render)

    return render_template(
        "index.html",
        servers=render_obj,
        messages=message_objects,
    )


################################
# RESTful VIEWS
################################

@app.route("/query", methods=["GET"])
def query():
    address = request.args.get("address")
    port = int(request.args.get("port"))
    conn = MinecraftServer(address, port)

    try:
        conn.ping()
    # except ConnectionRefusedError:
    # Commented out because for some reason on the production server,
    # attempting to catch this error causes the site to break and display
    # 'Internal Server Error'. Logs from such events say that
    # 'ConnectionRefusedError' is undefined, although there seem to be no
    # issues when testing locally.
    except:
        response = jsonify({
            "status": "Offline",
            "players_online": 0,
            "player_names": None,
        })
    else:
        q = conn.query()
        response = jsonify({
            "status": "Online",
            "players_online": q.players.online,
            "players_max": q.players.max,
            "player_names": q.players.names,
        })

    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0")
