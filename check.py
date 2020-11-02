class Person:

    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.__info()

    def print_info(self):
        print(f'name: {self.name}, age: {self.age}')

    def __info(self):
        print(f'info name: {self.name}, age: {self.age}')


class Worker(Person):

    def __init__(self, name, age, company):
        super().__init__(name, age)
        self.company = company

    def print_more_info(self):
        print(f'{self.name} works in {self.company}')


# worker1 = Worker('Vanya', 31, 'Google')
# worker1.print_info()
# worker1.print_info()
person1 = Person('John', 30)
# person1.print_info()
