from flask import g, request

from boilerplateapp.models.user import User
from boilerplateapp.responses import (
    bad_request,
    unauthorized,
    forbidden,
    not_found,
    method_not_allowed,
    conflict,
    unprocessable_entity,
)


def register_handlers(app):
    @app.before_request
    def default_login_required():
        # If this is an error or something else without a proper endpoint, just
        # return straight away.
        if not request.endpoint:
            return

        view = app.view_functions[request.endpoint]

        if getattr(view, 'login_exempt', False):
            return

        token_header = request.headers.get('Authorization')
        if not token_header or 'Bearer ' not in token_header:
            return unauthorized("Token not found or in wrong format.")

        token = token_header.replace('Bearer ', '')
        user = User.get_user_from_auth_token(token, salt='login')

        if not user:
            return unauthorized("Invalid user.")

        g.current_user = user

    @app.errorhandler(400)
    def handle_bad_request(e):
        return bad_request(e.name)

    @app.errorhandler(401)
    def handle_unauthorized(e):
        return unauthorized(e.name)

    @app.errorhandler(403)
    def handle_forbidden(e):
        return forbidden(e.name)

    @app.errorhandler(404)
    def handle_not_found(e):
        return not_found(e.name)

    @app.errorhandler(405)
    def handle_method_not_allowed(e):
        return method_not_allowed(e.name)

    @app.errorhandler(409)
    def handle_conflict(e):
        return conflict(e.name)

    @app.errorhandler(422)
    def handle_unprocessable_entity(err):
        # webargs attaches additional metadata to the `data` attribute
        data = getattr(err, 'data')
        if data:
            # Get validations from the ValidationError object
            messages = data['messages']
        else:
            messages = ['Invalid request']
        return unprocessable_entity(messages)