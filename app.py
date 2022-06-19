"""The application execution."""

from datetime import timedelta
from website import create_app


app = create_app()
app.permanent_session_lifetime = timedelta(days=2)


if __name__ == "__main__":
    # enable Debug mode: app.run(debug=True)
    app.run(debug=True)
