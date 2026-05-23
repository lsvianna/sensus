import os

from app import create_app


app = create_app()


if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "3000"))
    debug = os.getenv("DEBUG", "false").lower() in {"1", "true", "yes", "on"}

    app.run(host=host, port=port, debug=debug)
