from flask import render_template, Blueprint


errors = Blueprint("errors", __name__)


@errors.app_errorhandler(401)
def error_401(error):
    """The 401 app error handler.

    Args:
        error (parameter): The error to be handled.

    Returns:
        Renders a template with the error specific information.
    """
    return render_template("errors/401.html"), 401


@errors.app_errorhandler(403)
def error_403(error):
    """The 403 app error handler.

    Args:
        error (parameter): The error to be handled.

    Returns:
        Renders a template with the error specific information.
    """
    return render_template("errors/403.html"), 403


@errors.app_errorhandler(404)
def error_404(error):
    """The 404 app error handler.

    Args:
       error (parameter): The error to be handled.

    Returns:
        Renders a template with the error specific information.
    """
    return render_template("errors/404.html"), 404


@errors.app_errorhandler(500)
def error_500(error):
    """The 500 app error handler.

    Args:
        error (parameter): The error to be handled.

    Returns:
        Renders a template with the error specific information.
    """
    return render_template("errors/500.html"), 500
