from flask import Flask


def register(app:Flask):
    import auto_complete_api.endpoints.v0.messages as messages
    app.register_blueprint(messages.router, url_prefix='/v0/messages')
