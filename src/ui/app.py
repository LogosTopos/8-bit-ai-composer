"""
pywebview desktop app wrapper.
"""

import os

import webview

from .api import JsApi


def get_template_path() -> str:
    """Get absolute path to the HTML template."""
    return os.path.join(os.path.dirname(__file__), "templates", "index.html")


def launch() -> None:
    """Create and launch the pywebview window."""
    api = JsApi()
    html_path = get_template_path()

    window = webview.create_window(
        title="8-Bit Composer",
        url=html_path,
        js_api=api,
        width=900,
        height=550,
        resizable=True,
        min_size=(700, 450),
    )

    webview.start(debug=False)
