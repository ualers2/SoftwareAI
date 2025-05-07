import sys
import pytest
from typing_extensions import TypedDict
from agents import function_tool
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class Data(TypedDict):
    url: str

@function_tool
def fetch_dom(data: Data) -> str:
    """Carrega a página e retorna HTML bruto."""
    opts = Options()
    opts.add_argument("--headless")
    driver = webdriver.Chrome(options=opts)
    driver.get(data.get("url"))
    html = driver.page_source
    driver.quit()
    return html