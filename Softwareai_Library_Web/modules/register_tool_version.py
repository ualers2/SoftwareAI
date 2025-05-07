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


def register_tool_version(tool_id, 
                        new_hash, 
                        appcompany,
                        tool_metadata,
                        tool_code,
                        tool_compose


                    ):
    ref = db.reference(f"tool_hashes/{tool_id}/versions", app=appcompany)

    # Verifica se já existe esse hash (não registra duplicado)
    existing_versions = ref.get() or {}
    for version, data in existing_versions.items():
        if data.get('hash') == new_hash:
            print(f"[skip] Hash já registrado para {tool_id}")
            return

    # Gera nova versão incremental
    version_number = len(existing_versions) + 1
    version_name = f"v{version_number}"

    ref.child(version_name).set({
        "tool_compose": tool_compose,
        "tool_code": tool_code,
        "tool_metadata": tool_metadata,
        "hash": new_hash,
        "timestamp": time.time()
    })

    # Atualiza referência para última versão
    db.reference(f"tool_hashes/{tool_id}/latest", app=appcompany).set(version_name)

    print(f"[new] Registrada nova versão {version_name} para {tool_id}")