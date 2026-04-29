import json
import os
import shutil
import sys
from pathlib import Path

# Get project root (2 levels up from this script)
script_dir = Path(__file__).resolve().parent
project_root = script_dir.parent.parent
sys.path.append(str(project_root / "backend" / "src"))

try:
    from main import app

    def export_openapi():
        # 1. Altere a parte do "temporary directory"
        export_dir = os.environ.get("EXPORT_DIR")
        if export_dir:
            base_dir = Path(export_dir)
        else:
            base_dir = project_root / "api-client"

        base_dir.mkdir(parents=True, exist_ok=True)

        # Generate openapi.json
        json_file = base_dir / "openapi.json"
        with open(json_file, "w") as f:
            json.dump(app.openapi(), f, indent=2)
        os.chmod(json_file, 0o666)
        print(f"Success: {json_file}")

        # Generate Bruno environment
        env_dir = base_dir / "blood-donation-api" / "environments"
        env_dir.mkdir(parents=True, exist_ok=True)
        try:
            os.chmod(env_dir, 0o777)
        except Exception:
            pass

        # Managed localhost environment
        localhost_file = env_dir / "localhost.bru"

        # 2. vamos trocar o arquivo "localhost.bru" gerado pelo backup que fizemos
        backup_file = Path("/tmp/localhost.bru.bak")
        if backup_file.exists():
            shutil.copy(backup_file, localhost_file)
            print(f"Restored backup from {backup_file} to {localhost_file}")
        else:
            localhost_content = "vars {\n  baseUrl: http://localhost:8000\n}\n"
            with open(localhost_file, "w") as f:
                f.write(localhost_content)
            print(f"Success: {localhost_file}")

        # Ensure permissions for all environment files
        for file in [localhost_file]:
            try:
                if file.exists():
                    os.chmod(file, 0o666)
            except Exception:
                pass

    if __name__ == "__main__":
        export_openapi()

except Exception as e:
    print(f"Error: {e}")
