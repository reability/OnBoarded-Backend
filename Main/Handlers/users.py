from Common.Endpoint.rest_endpoint import RestEndpoint
from Main.Models.model import User, session
from aiohttp.web import Response
import json


class Rest_user_endpoint(RestEndpoint):

    def __init__(self, resource):
        super().__init__()
        self.resource = resource

    async def get(self, instance_id):
        instance = session.query(User).filter(User.id == instance_id).first()
        if not instance:
            return Response(status=404, body=json.dumps({'not found': 404}), content_type='application/json')

        data = self.resource.render_and_encode(instance)
        return Response(status=200, body=data, content_type='application/json')