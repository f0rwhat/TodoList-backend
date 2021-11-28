class GenericException(Exception):
    msg: str
    code: int


class ProjectNotFoundException(GenericException):
    code = 404
    msg = "Указанный проект не существует."


class UserNotInProjectException(GenericException):
    code = 404
    msg = "Пользователя нет в проекте."


class UserIsAlreadyInProjectException(GenericException):
    code = 400
    msg = "Пользователь уже был добавлен в проект"


class CantDeleteMaintainerFromProjectException(GenericException):
    code = 400
    msg = "Владелец проекта не может быть удален из проекта!"


class TaskNotFoundException(GenericException):
    code = 404
    msg = "Указанной задачи не существует."


class UniqueDataException(GenericException):
    code = 422
    msg = "Почта уже используется."


class UserNotFoundException(GenericException):
    msg = "Пользователь не найден."
    code = 404


class WrongDataException(GenericException):
    msg = "Неверная почта или пароль."
    code = 400


class JWTExpiredException(GenericException):
    msg = "Код недействителен."
    code = 400


class UnauthorizedAccess(GenericException):
    msg = "Доступ запрещен."
    code = 401

