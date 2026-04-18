import json
import os
import sys

# Adiciona o diretório src ao path
sys.path.append(os.path.join(os.getcwd(), "backend", "src"))

try:
    from main import app

    def export_openapi():
        openapi_schema = app.openapi()
        with open("openapi.json", "w") as f:
            json.dump(openapi_schema, f, indent=2)
        print("openapi.json exportado com sucesso!")

    if __name__ == "__main__":
        export_openapi()
except ImportError as e:
    print(f"Erro de importação: {e}")
    print(f"PYTHONPATH atual: {sys.path}")
except Exception as e:
    print(f"Erro inesperado: {e}")
