import json
import os
import sys
from pathlib import Path

# Get project root (2 levels up from this script)
script_dir = Path(__file__).resolve().parent
project_root = script_dir.parent.parent
sys.path.append(str(project_root / "backend" / "src"))

try:
    from main import app

    def export_openapi():
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

        # 1. Managed localhost environment
        localhost_file = env_dir / "localhost.bru"
        localhost_content = "vars {\n  baseUrl: http://localhost:8000\n}\n"
        with open(localhost_file, "w") as f:
            f.write(localhost_content)
        print(f"Success: {localhost_file}")

        # 2. User variables (created only if it doesn't exist)
        user_vars_file = env_dir / "your-variables-here.bru"
        if not user_vars_file.exists():
            user_vars_content = "vars {\n  # Add your variables here\n  # baseUrl: http://localhost:8000\n}\n"
            with open(user_vars_file, "w") as f:
                f.write(user_vars_content)
            print(f"Success: {user_vars_file}")
        else:
            print(f"Skipped: {user_vars_file} (already exists)")

        # Ensure permissions for all environment files
        for file in [localhost_file, user_vars_file]:
            try:
                if file.exists():
                    os.chmod(file, 0o666)
            except Exception:
                pass

        # 3. Cleanup old Local.bru if exists
        old_local = env_dir / "Local.bru"
        if old_local.exists():
            old_local.unlink()
            print(f"Removed legacy file: {old_local}")

    if __name__ == "__main__":
        export_openapi()

except Exception as e:
    print(f"Error: {e}")
