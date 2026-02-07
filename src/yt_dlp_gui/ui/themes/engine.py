from pathlib import Path
import json

def load_stylesheet(theme_name: str="dark") -> str:

  base_path = Path(__file__).parent
  variables = base_path / f"variables_{theme_name}.json"
  glob_vars = base_path / "globals.json"

  tokens = {}
  if variables.exists():
    tokens.update(json.load(variables.open()))
  if glob_vars.exists():
    tokens.update(json.load(glob_vars.open()))

  qss = ""
  files = ("main.qss", "input_section.qss", "selection_menu.qss")

  for file in files:
    f_path = base_path / file
    qss += f_path.read_text()

  for key, value in tokens.items():
    qss = qss.replace(f"{{{{{key}}}}}", value)

  return qss