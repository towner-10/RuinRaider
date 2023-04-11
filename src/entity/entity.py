import uuid
from typing import TypeVar

# Generic type variable for components.
T = TypeVar('T')

# Base class for all entities that allows for easy component storage and retreival
class Entity:
    def __init__(self, *components: T):
        """Create a new entity with the given components. Creates a new UUID for the entity."""
        self.components = {}
        self.id = uuid.uuid4()

        for component in components:
            self.set(component)

    def set(self, component: T) -> None:
        """Add a component to the entity."""
        key = type(component)
        self.components[key] = component

    def get(self, component: T) -> T:
        """Get a component from the entity."""
        return self.components[component]

    def has(self, component: T) -> bool:
        """Check if the entity has a component."""
        return self.get(component) is not None