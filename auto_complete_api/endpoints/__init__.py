from flask import Flask


def register(app:Flask):
    import auto_complete_api.endpoints.v0 as v0
    v0.register(app)
