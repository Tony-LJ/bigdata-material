import json

class MyClass:
    def __init__(self, name, age, is_student):
        self.name = name
        self.age = age
        self.is_student = is_student

    def to_dict(self):
        return {
            'name': self.name,
            'age': self.age,
            'is_student': self.is_student
        }

obj = MyClass(name="Alice", age=30, is_student=True)
json_str = json.dumps(obj.to_dict())
print(json_str)