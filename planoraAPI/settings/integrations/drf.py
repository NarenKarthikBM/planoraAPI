REST_FRAMEWORK = {
    # * Custom UJSON parser and renderer classes
    "DEFAULT_RENDERER_CLASSES": [
        "planoraAPI.settings.custom_DRF_settings.renderers.UJSONRenderer",
    ],
    "DEFAULT_PARSER_CLASSES": [
        "planoraAPI.settings.custom_DRF_settings.parsers.UJSONParser",
    ],
    # * Custom authentication class
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "planoraAPI.settings.custom_DRF_settings.authentication.TokenAuthentication",
    ],
}
