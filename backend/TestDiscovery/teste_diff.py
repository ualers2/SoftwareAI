from Agents.gpt_engineer.core.diffprocessor import DiffProcessor
import os
import tempfile

# os.chdir()
# diff_file = os.path.join(os.path.dirname(__file__), 'example8', "teste.diff")
diff_content = """
--- /dev/null
+++ main.py
@@ -0,0 +1,10 @@
+def hello_world():
+    print("Hello, World!")
+
+
+def main():
+    hello_world()
+
+
+if __name__ == "__main__":
+    main()
"""
repo_path = os.path.join(os.path.dirname(__file__), 'example8')

with tempfile.NamedTemporaryFile("w+", delete=False, encoding="utf-8", suffix=".diff") as tmp_diff:
    tmp_diff.write(diff_content)
    tmp_diff_path = tmp_diff.name

dp = DiffProcessor(diff_path=tmp_diff_path)
dp.parse()
print(dp.summary())
dp.validate()
dp.apply(repo_path)

os.remove(tmp_diff_path)