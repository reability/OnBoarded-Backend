from RestEndpoint import RestEndpoint
from model import User, session
from aiohttp.web import Response
import json
from aiohttp.web_urldispatcher import UrlDispatcher
from collections import OrderedDict


class user_rest_endpoint(RestEndpoint):

    def __init__(self, resource):
        super().__init__()
        self.resource = resource

    async def get(self, instance_id):
        instance = session.query(User).filter(User.id == instance_id).first()
        if not instance:
            return Response(status=404, body=json.dumps({'not found': 404}), content_type='application/json')

        data = self.resource.render_and_encode(instance)
        return Response(status=200, body=data, content_type='application/json')

    async def post(self, request):
        data = await request.json()





class UsersRestResource:
    def __init__(self, users, factory, collection, properties, id_field):
        self.users = users
        self.factory = factory
        self.collection = collection
        self.properties = properties
        self.id_field = id_field

        self.instance_endpoint = user_rest_endpoint(self)

    def register(self, router: UrlDispatcher):
        router.add_route('*', '/{users}/{{instance_id}}'.format(users=self.users), self.instance_endpoint.dispatch)

    def render(self, instance):
        return OrderedDict((users, getattr(instance, users)) for users in self.properties)

    @staticmethod
    def encode(data):
        return json.dumps(data, indent=4).encode('utf-8')

    def render_and_encode(self, instance):
        return self.encode(self.render(instance))
