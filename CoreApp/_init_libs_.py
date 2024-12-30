
#########################################
# IMPORT Libs
import importlib
import pkgutil
import os
import subprocess
import threading
import asyncio
import json
from firebase_admin import credentials, initialize_app, storage, db, delete_app
from openai import OpenAI
import time
import pandas as pd
import shutil
import tiktoken
from github import Github
import re
import requests
import base64
import random
from datetime import datetime, timedelta
import struct
from dotenv import load_dotenv, find_dotenv
import git
from requests.auth import HTTPBasicAuth
import sys
import json
import ast
import os
import subprocess
import platform
from firebase_admin import credentials, initialize_app, storage, db, delete_app
import concurrent.futures
from PySide2extn.RoundProgressBar import roundProgressBar #IMPORT THE EXTENSION LIBRARY
from PySide2.QtCore import QTimer, Signal, QThread
from PySide2.QtWidgets import QFileDialog
import sys
import json
import time
import os
import subprocess
import platform
from firebase_admin import credentials, initialize_app, storage, db, delete_app
import concurrent.futures
import hashlib
from typing import Optional, List, Union
from typing_extensions import override
from openai import AssistantEventHandler, OpenAI
from openai.types.beta.threads import Text, TextDelta
from openai.types.beta.threads.runs import ToolCall, ToolCallDelta
#########################################
