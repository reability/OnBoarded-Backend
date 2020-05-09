import json
from aiohttp.web_urldispatcher import UrlDispatcher
from collections import OrderedDict
from Main.Handlers.users import Rest_user_endpoint


class UsersRestResource:
    def __init__(self, users, factory, collection, properties, id_field):
        self.users = users
        self.factory = factory
        self.collection = collection
        self.properties = properties
        self.id_field = id_field

        self.instance_endpoint = Rest_user_endpoint(self)

    def register(self, router: UrlDispatcher):
        router.add_route('*', '/{users}/{{instance_id}}'.format(users=self.users), self.instance_endpoint.dispatch)

    def render(self, instance):
        return OrderedDict((users, getattr(instance, users)) for users in self.properties)

    @staticmethod
    def encode(data):
        return json.dumps(data, indent=4).encode('utf-8')

    def render_and_encode(self, instance):
        return self.encode(self.render(instance))
