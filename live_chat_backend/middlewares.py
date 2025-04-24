import jwt
from urllib.parse import parse_qs
from django.db import close_old_connections
from django.contrib.auth import get_user_model
from channels.db import database_sync_to_async

from rest_framework_simplejwt.tokens import AccessToken

import logging
import json

logger = logging.getLogger("django.request")


class RequestLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Log request details
        logger.info(
            f"Request: {request.method} {request.path} from {request.META.get('REMOTE_ADDR')}"
        )

        response = self.get_response(request)

        # Safe JSON logging
        content_type = response.get("Content-Type", "")
        if "application/json" in content_type:
            try:
                response_body = json.loads(response.content.decode("utf-8"))
                preview = (
                    json.dumps(response_body)[:300] + "..."
                    if len(json.dumps(response_body)) > 300
                    else response_body
                )
                logger.info(
                    f"Response: {response.status_code} for {request.path}, JSON: {preview}"
                )
            except Exception as e:
                logger.warning(f"Could not parse JSON for {request.path}: {str(e)}")
        else:
            logger.info(
                f"Response: {response.status_code} for {request.path}, non-JSON content"
            )

        return response


# User WS Connection Middleware
class UserMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        close_old_connections()

        query_params = parse_qs(scope["query_string"].decode("utf8"))
        token = query_params.get("token", [None])[0]
        reciever_id = query_params.get("reciever_id", [None])[0]
        scope["reciever_id"] = reciever_id

        if token:
            try:
                access_token = AccessToken(token)
                user_id = access_token["user_id"]
                user = await database_sync_to_async(get_user_model().objects.get)(
                    id=user_id
                )
                scope["user"] = user
            except jwt.ExpiredSignatureError:
                return None
            except jwt.InvalidTokenError:
                return None

        return await self.app(scope, receive, send)
