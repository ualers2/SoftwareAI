import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

os.chdir(os.path.join(os.path.dirname(__file__)))
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), 'keys.env'))

# Defina o schema Pydantic para o diff
class DiffOutput(BaseModel):
    filename: str
    diff: str

# Cria o LLM
llm = ChatOpenAI(
    model="gpt-5-nano",
    temperature=0,
    api_key=os.getenv("OPENAI_API_KEY")
)

# Bind do LLM a um parser Pydantic
structured_llm = llm.with_structured_output(DiffOutput)

# Prompt
prompt = """Crie um diff que adicione a função hello_world() em main.py




You will output the content of each file necessary to achieve the goal, including ALL code.
Output requested code changes and new code in the unified "git diff" syntax. Example:

```diff
--- example.txt
+++ example.txt
@@ -6,3 +6,4 @@
     line content A
     line content B
+    new line added
-    original line X
+    modified line X with changes
@@ -26,4 +27,5 @@
         condition check:
-            action for condition A
+            if certain condition is met:
+                alternative action for condition A
         another condition check:
-            action for condition B
+            modified action for condition B
```

Example of a git diff creating a new file:

```diff
--- /dev/null
+++ new_file.txt
@@ -0,0 +1,3 @@
+First example line
+
+Last example line
```

RULES:
-A program will apply the diffs you generate exactly to the code, so diffs must be precise and unambiguous!
-Every diff must be fenced with triple backtick ```.
-The file names at the beginning of a diff, (lines starting with --- and +++) is the relative path to the file before and after the diff.
-LINES TO BE REMOVED (starting with single -) AND LINES TO BE RETAIN (no starting symbol) HAVE TO REPLICATE THE DIFFED HUNK OF THE CODE EXACTLY LINE BY LINE. KEEP THE NUMBER OF RETAIN LINES SMALL IF POSSIBLE.
-EACH LINE IN THE SOURCE FILES STARTS WITH A LINE NUMBER, WHICH IS NOT PART OF THE SOURCE CODE. NEVER TRANSFER THESE LINE NUMBERS TO THE DIFF HUNKS.
-AVOID STARTING A HUNK WITH AN EMPTY LINE.
-ENSURE ALL CHANGES ARE PROVIDED IN A SINGLE DIFF CHUNK PER FILE TO PREVENT MULTIPLE DIFFS ON THE SAME FILE.

"""

# Chamada
result = structured_llm.invoke(prompt)

# O resultado já vem como objeto DiffOutput
print(result.filename)
print(result.diff)
