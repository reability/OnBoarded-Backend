from aiohttp.web import Application, run_app, Response
from aiohttp import web

from Main.Resources.users_resource import UsersRestResource
from Main.Models.model import User


path_to_static_folder = r"C:\Users\vanur\PycharmProjects\OnBoarded-Backend\Static"


async def test(request):
    return Response(text="Hello")


users = {}
app = Application()

app.router.add_route("*", "/", test)

app.add_routes([web.static('/static', path_to_static_folder)])

resource = UsersRestResource('users', User, users, ('firstname', 'lastname', 'middlename', 'companytitle', 'jobtitle', 'isAdviser'), 'lastname')
resource.register(app.router)

web.static('/static', path_to_static_folder, follow_symlinks=True)
web.static('/static', path_to_static_folder, show_index=True)

if __name__ == '__main__':

    run_app(app, port=8181, host="127.0.0.1")