import Class.SagaClass as SagaClass


class Parent(SagaClass):
    name = 'parent'

    def get_name(self):
        print(self.name)
        print(self.get_param("name"))

    def set_name(self, name):
        self.name = name

    def sayhello(self):
        print("hello, parent "+self.name)

    def sayhi(self):
        print("hi parent "+self.name)


class Child(Parent):
    def sayhello(self):
        print("hello, child "+self.name)

    def sayname(self):
        print("hello name = "+self.name)

    def setname(self, name):
        self.name = name


c = Child()
c.sayhello()
c.sayhi()
c.sayname()
c.setname("child")
c.sayhello()
c.sayhi()
c.sayname()