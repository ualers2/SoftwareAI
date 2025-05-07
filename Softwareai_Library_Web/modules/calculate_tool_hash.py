import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from firebase_admin import credentials, db, initialize_app
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, make_response, Response
from flask_cors import CORS
from datetime import timedelta
import os
import json
import yaml
from dotenv import load_dotenv
import logging
import sys
import importlib.util
import inspect
import hashlib
import io

def calculate_tool_hash(tool_path):
    sha256 = hashlib.sha256()

    for root, _, files in os.walk(tool_path):
        for file in sorted(files):  # importante manter a ordem
            if file.endswith('.py'):
                full_path = os.path.join(root, file)
                with open(full_path, 'rb') as f:
                    while chunk := f.read(8192):
                        sha256.update(chunk)

    return sha256.hexdigest()
