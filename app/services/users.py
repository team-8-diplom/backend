from app.dependencies.repositories import UserRepository, UserRepositoryDep


class UserService:
    __user_repository: UserRepository

    def __init__(self, user_repository: UserRepositoryDep):
        self.__user_repository = user_repository
