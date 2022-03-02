from typing import Type

from container import container


def container_resolve(implementation: Type):
    async def resolver():
        return container.resolve(implementation)

    return resolver
