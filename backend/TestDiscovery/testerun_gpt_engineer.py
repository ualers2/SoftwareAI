import os 
from dotenv import load_dotenv

os.chdir(os.path.join(os.path.dirname(__file__)))
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), 'Keys', 'keys.env'))

from Agents.gpt_engineer.applications.cli.main import run_gpt_engineer

default_prompt = """
Product Description (Front-End): Multi-user system (doctors and patients) for online appointment scheduling.
The front-end should be developed in Vite + React, including:

- Responsive and accessible interface for desktop and mobile.
- Reusable and modularized components.
- User management (registration, login, profile).
- Appointment scheduling.
- Payments via Stripe.
- Global state and data management.
- Minimal observability on the front-end.
- Support for authentication and authorization of different user profiles.
- Best UI/UX practices, including feedback for user actions.
- Organized folder structure and easy maintenance.
"""

with open("errorr.txt", "r", encoding='utf-8') as err:
    error = err.read()
improvment_prompt = f"""
pense passo a passo para resolver o erro abaixo e corrija os arquivos problematicos de forma proativa:
{error}
"""

result = run_gpt_engineer(
    project_path="./example8",
    # default_prompt=default_prompt,
    default_improve_prompt=improvment_prompt,
    improve_mode=True,
    model="gpt-5-nano",
    auto_apply_changes=True,
    skip_entrypoint_execution=True,  # Pula confirmações
    verbose=True,
    debug=True
)

if result.success:
    print("Success!")
    print("Files created:", list(result.files_dict.keys()))
else:
    print("Error:", result.error_message)