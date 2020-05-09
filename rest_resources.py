import inspect
import json
from collections import OrderedDict
from model import User, session
from aiohttp.web import Request, Response
from aiohttp.web_urldispatcher import UrlDispatcher
from RestEndpoint import RestEndpoint

__version__ = '0.1.0'

DEFAULT_METHODS = ('GET', 'POST', 'PUT', 'DELETE')


class CollectionEndpoint(RestEndpoint):
    def __init__(self, resource):
        super().__init__()
        self.resource = resource

    async def get(self) -> Response:
        data = []

        users = session.query(User).all()
        for instance in self.resource.collection.values():
            data.append(self.resource.render(instance))
        data = self.resource.encode(data)
        return Response ( status=200, body=self.resource.encode({
            'notes': [
                {'id': user.id, 'title': user.title, 'description': user.description,
                'created_at': user.created_at, 'created_by': user.created_by, 'priority': user.priority}

                    for user in session.query(User)

                    ]
            }), content_type='application/json')


    async def post(self, request):
        data = await request.json()
        note=User(title=data['title'], description=data['description'], created_at=data['created_at'], created_by=data['created_by'], priority=data['priority'])
        session.add(note)
        session.commit()

        return Response(status=201, body=self.resource.encode({
            'notes': [
                {'id': note.id, 'title': note.title, 'description': note.description,
                'created_at': note.created_at, 'created_by': note.created_by, 'priority': note.priority}

                    for note in session.query(Note)

                    ]
            }), content_type='application/json')


class InstanceEndpoint(RestEndpoint):
    def __init__(self, resource):
        super().__init__()
        self.resource = resource

    async def get(self, instance_id):
        instance = session.query(Note).filter(Note.id == instance_id).first()
        if not instance:
            return Response(status=404, body=json.dumps({'not found': 404}), content_type='application/json')
        data = self.resource.render_and_encode(instance)
        return Response(status=200, body=data, content_type='application/json')

    async def put(self, request, instance_id):

        data = await request.json()

        note = session.query(Note).filter(Note.id == instance_id).first()
        note.title = data['title']
        note.description = data['description']
        note.created_at = data['created_at']
        note.created_by = data['created_by']
        note.priority = data['priority']
        session.add(note)
        session.commit()

        return Response(status=201, body=self.resource.render_and_encode(note),
                        content_type='application/json')

    async def delete(self, instance_id):
        note = session.query(Note).filter(Note.id == instance_id).first()
        if not note:
            abort(404, message="Note {} doesn't exist".format(id))
        session.delete(note)
        session.commit()
        return Response(status=204)


class RestResource:
    def __init__(self, notes, factory, collection, properties, id_field):
        self.notes = notes
        self.factory = factory
        self.collection = collection
        self.properties = properties
        self.id_field = id_field

        self.collection_endpoint = CollectionEndpoint(self)
        self.instance_endpoint = InstanceEndpoint(self)

    def register(self, router: UrlDispatcher):
        router.add_route('*', '/{notes}'.format(notes=self.notes), self.collection_endpoint.dispatch)
        router.add_route('*', '/{notes}/{{instance_id}}'.format(notes=self.notes), self.instance_endpoint.dispatch)

    def render(self, instance):
        return OrderedDict((notes, getattr(instance, notes)) for notes in self.properties)

    @staticmethod
    def encode(data):
        return json.dumps(data, indent=4).encode('utf-8')

    def render_and_encode(self, instance):
        return self.encode(self.render(instance))