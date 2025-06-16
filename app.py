import os
import json
import tempfile
import subprocess
from flask import Flask, request, jsonify

app = Flask(__name__)

def validate_script(script):
    if not isinstance(script, str):
        return False, "Script must be a string."
    if "def main()" not in script:
        return False, "Script must contain a 'main()' function."
    return True, None

@app.route("/execute", methods=["POST"])
def execute_script():
    data = request.get_json()
    if not data or "script" not in data:
        return jsonify({"error": "Missing 'script' field"}), 400

    script = data["script"]
    valid, msg = validate_script(script)
    if not valid:
        return jsonify({"error": msg}), 400

    with tempfile.TemporaryDirectory() as tmpdir:
        script_path = os.path.join(tmpdir, "script.py")
        with open(script_path, "w") as f:
            f.write(script + "\n\nimport json\nprint(json.dumps(main()))")

        cmd = [
            "nsjail",
            "--config", "/app/nsjail.cfg",
            "--",
            "/usr/local/bin/python3", script_path
        ]

        try:
            result = subprocess.run(cmd, capture_output=True, timeout=10, text=True)

            if result.returncode != 0:
                return jsonify({
                    "error": "Execution failed",
                    "stderr": result.stderr
                }), 400

            # Parse stdout and ensure it's a JSON object (dict)
            try:
                parsed_output = json.loads(result.stdout.strip())
            except json.JSONDecodeError as e:
                return jsonify({
                    "error": "Output is not valid JSON",
                    "stderr": result.stderr,
                    "raw_output": result.stdout.strip()
                }), 400

            if not isinstance(parsed_output, dict):
                return jsonify({
                    "error": "main() must return a JSON object (dictionary).",
                    "returned_type": str(type(parsed_output)),
                    "raw_output": parsed_output
                }), 400

            return jsonify({"result": parsed_output, "stdout": result.stderr})

        except subprocess.TimeoutExpired:
            return jsonify({"error": "Execution timed out"}), 408
