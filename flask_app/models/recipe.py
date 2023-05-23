from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Recipe:
    db="recipes_schema"
    def __init__ (self,data):
        self.id = data['id']
        self.name = data['name']
        self.under = data['under']
        self.date_made= data['date_made']
        self.description = data['description']
        self.instruction = data['instruction']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.creator = None

    @classmethod
    def save_recipe(cls,data):
        query = "INSERT INTO recipes (name, under, description, instruction, date_made, user_id ) VALUES (%(name)s,%(under)s,%(description)s,%(instruction)s,%(date_made)s, %(user_id)s)"
        results = connectToMySQL(cls.db).query_db(query,data)
        return results
    
    @classmethod
    def get_all_recipe(cls):
        query = "SELECT * FROM recipes LEFT JOIN users ON users.id = recipes.user_id;"
        results=connectToMySQL(cls.db).query_db(query)
        recipes=[]
        for recipe in results:
            user_data= {
                "id":recipe['user_id'],
                "first_name":recipe['first_name']
            }
            this_recipe=cls(recipe)
            this_recipe.creator=user_data
            recipes.append(this_recipe)
        return recipes
    
    @classmethod
    def get_recipe_by_id(cls,data):
        query = "SELECT * FROM recipes LEFT JOIN users ON recipes.user_id = users.id WHERE recipes.id = %(id)s;"
        results=connectToMySQL(cls.db).query_db(query,data)
        result=results[0]
        print("*******************")
        print(result)
        this_recipe=cls(result)
        user_data={
            "id":result['users.id'],
            "first_name":result['first_name']
        }
        this_recipe.creator=user_data
        return this_recipe
    @classmethod
    def edit_recipe(cls, data):
        query = """
                UPDATE recipes 
                SET name = %(name)s,
                description = %(description)s,
                instruction = %(instruction)s,
                date_made = %(date_made)s,
                under = %(under)s
                WHERE id = %(id)s;
                """
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def delete(cls,data):
        query = "DELETE FROM recipes WHERE id=%(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)

    @staticmethod
    def validate_recipe(data):
        is_valid = True
        if len(data['name'])<3:
            is_valid = False
            flash("Name must be at least 3 charactor.","recipe")
        if len(data['description'])<3:
            is_valid = False
            flash("Description must be at least 3 charactor.","recipe")
        if len(data['instruction'])<3:
            is_valid = False
            flash("Instructions must be at least 3 charactor.","recipe")
        if data['date_made'] == "":
            is_valid= False
            flash("Please input made date. ")
        if 'under' not in data:
            is_valid=False
            flash("Please input cook time.")
        return is_valid
            

    