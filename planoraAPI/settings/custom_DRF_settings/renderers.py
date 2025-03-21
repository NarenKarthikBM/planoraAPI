from typing import Any, Mapping, Optional, Union

import ujson
from rest_framework.renderers import JSONRenderer

__all__ = ["UJSONRenderer"]


class UJSONRenderer(JSONRenderer):
    """
    Renderer which serializes to JSON.
    Applies JSON's backslash-u character escaping for non-ascii characters.
    Uses the blazing-fast ujson library for serialization.
    """

    # Controls whether forward slashes (/) are escaped.
    escape_forward_slashes: bool = False
    # Used to enable special encoding of "unsafe" HTML characters into safer
    # Unicode sequences.
    encode_html_chars: bool = False

    def render(
        self,
        data: Union[dict, None],
        accepted_media_type: Optional[str] = None,
        renderer_context: Optional[Mapping[str, Any]] = None,
    ) -> bytes:
        if data is None:
            return bytes()

        accepted_media_type = accepted_media_type or ""
        renderer_context = renderer_context or {}
        indent = self.get_indent(accepted_media_type, renderer_context)
        encoder = self.encoder_class()

        ret = ujson.dumps(
            data,
            ensure_ascii=self.ensure_ascii,
            escape_forward_slashes=self.escape_forward_slashes,
            encode_html_chars=self.encode_html_chars,
            indent=indent or 0,
            default=encoder.default,  # type: ignore
        )

        # force return value to unicode
        if isinstance(ret, str):
            ret = ret.replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")
            return bytes(ret.encode("utf-8"))
        return ret
