import punq

container = punq.Container()


def register(*args, **kwargs):
    if len(args) == 1 and not kwargs and callable(args[0]):
        cls = args[0]

        container.register(cls)

        return cls
    raise NotImplementedError("Custom class registration is not supported yet")
