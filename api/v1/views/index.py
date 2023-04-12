#!/usr/bin/python3
"""This module defines the routes for app_views"""
from flask import jsonify
from . import app_views


@app_views.route("/status", strict_slashes=False)
def show_status():
    return jsonify({"status": "OK"})
