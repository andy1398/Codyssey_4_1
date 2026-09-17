#category.py
""" 카테고리 관리 """

class Category:
    def __init__(self):
        self.category = []
        self.name=[]
        self.type=[]
        
    def add_category(self,id, name, type):
        num=len(self.category)        
        for i in range(len(self.category)):
            if(self.category[0]==id):
                print("이미 존재하는 내역입니다.")
                return
        name_index = self.add_name(name,num)
        type_index = self.add_type(type,num)
        self.category.append((id, name_index, type_index))
               
    def add_name(self,name,num):
        for i in range(num):
            if self.name[i]==name:
                return i
        self.name.append(name)
        return num+1
    
    def add_type(self,type,num):
        for i in range(num):
            if self.type[i]==type:
                return i
        self.type.append(type)
        return num+1