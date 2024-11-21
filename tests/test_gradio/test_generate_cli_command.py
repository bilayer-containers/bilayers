import os
import pytest
import shutil
from unittest.mock import MagicMock, patch
from gradio import Error
from src.build.parse.gradio_template.py.j2 import generate_cli_command  
