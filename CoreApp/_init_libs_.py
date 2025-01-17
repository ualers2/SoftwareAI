
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
import schedule
from typing import Optional, List, Union
from typing_extensions import override
from openai import AssistantEventHandler, OpenAI
from openai.types.beta.threads import Text, TextDelta
from openai.types.beta.threads.runs import ToolCall, ToolCallDelta


from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle, HRFlowable
)
from reportlab.pdfgen import canvas
## IMPORTS Libs
import sys
import os
import subprocess
from typing import Dict, Any
import time
import psutil
import GPUtil
import math
import hashlib
from typing import Dict, Any
import os
import subprocess
import requests
import json
import requests
import re
from firebase_admin import credentials, initialize_app, storage, db, delete_app
import concurrent.futures
from reportlab.platypus import PageBreak
from reportlab.lib.colors import Color, black, white


from reportlab.platypus import Image as Imagereportlab
from reportlab.platypus import PageBreak, Table, TableStyle,Preformatted,  Paragraph, HRFlowable, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib.utils import ImageReader

from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate, Paragraph
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import BaseDocTemplate, Paragraph, PageBreak, Frame
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

import requests
import json
import random
import re
import os
import time
from firebase_admin import credentials, storage, db
import requests
import firebase_admin
import obsws_python as obs
from openai import OpenAI
import base64
import requests
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from termcolor import cprint
from reportlab.platypus import NextPageTemplate

from huggingface_hub import InferenceClient
from huggingface_hub import login
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from concurrent.futures import ThreadPoolExecutor, as_completed
from reportlab.pdfgen import canvas

import time
import random
from openai import OpenAI


import json

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters


from firebase_admin import credentials, initialize_app, storage, db

from datetime import datetime, timedelta
from PIL import Image 
########################################################################
## IMPORTAÇÃO DE BIBLIOTECAS
########################################################################

# Bibliotecas padrão do Python

import os
import sys
import json
import time
import random
import re
import subprocess
import platform
import tempfile
from datetime import datetime, timedelta
from typing import Dict, Any
from collections import defaultdict
from queue import Queue, Empty
import threading

# Bibliotecas de terceiros
try:
    import requests
    import GPUtil
    import shutil
    import whisper
    import glob
    import math
    import torch
    import traceback
    import hashlib
    from concurrent.futures import ThreadPoolExecutor
    import uiautomator2 as u2
    import cv2
    import numpy as np
    import wave
    import srt
    import yt_dlp
    import psutil
    import schedule
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload

    

    import websockets
    import asyncio
    import av
    import logging
    import io


    from dotenv import load_dotenv, find_dotenv
    from firebase_admin import credentials, initialize_app, storage, db, delete_app
    from transformers import (
        AutoModelForSpeechSeq2Seq,
        AutoTokenizer,
        AutoFeatureExtractor,
        pipeline,
    )
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    from PySide2.QtWidgets import *
    from PySide2 import QtWidgets, QtCore, QtGui
    from PySide2.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEngineSettings, QWebEngineScript

    from proglog import ProgressBarLogger
except ImportError as e:
    print(f"Erro ao importar bibliotecas: {e}")
    
#########################################
