from aiohttp.web import Application, run_app, Response

from users_resource import UsersRestResource
from model import User

from sqlalchemy import engine_from_config

async def test(request):
    return Response(text="Hello")

users = {
    User("Владыка", "Кожемякин", "Олегович", "1", "МТС", "12", "134", "Программист высшего ранга")
}
app = Application()

app.router.add_route("*", "/", test)

resource = UsersRestResource('users', User, users, ('firstname', 'lastname', 'middlename', 'companytitle', 'jobtitle'), 'lastname')
resource.register(app.router)

if __name__ == '__main__':

    run_app(app, port=8181, host="127.0.0.1")