class Person:
    def __init__(self, name=None):
        self.name = name

class DictMixin:
    def to_dict(self):
        return vars(self)

class JsonMixin:
    def to_json(self):
        import json
        return json.dumps(self.to_dict())

class Empleado(Person, DictMixin, JsonMixin):
    def __init__(self, name, skills, family):
        super().__init__(name)
        self.skills = skills
        self.family = family

empleado = Empleado("Juan", ["Python", "Django"], {"esposa": "María"})
print(empleado.to_dict())
# {'nombre': 'Juan', 'skills': ['Python', 'Django'], 'familia': {'esposa': 'María'}}

print(empleado.to_json())
# {"nombre": "Juan", "skills": ["Python", "Django"], "familia": {"esposa": "María"}}
