from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models import recipe,user
from flask_bcrypt import Bcrypt
bcrypt=Bcrypt(app)


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    recipes_list = recipe.Recipe.get_all_recipe()
    return render_template('dashboard.html', recipes_list=recipes_list)

@app.route('/recipes/<int:id>')
def view_recipes(id):
    data = {
        'id':id
    }
    recipe_info = recipe.Recipe.get_recipe_by_id(data)  
    return render_template("view_recipe.html",recipe_info=recipe_info)

@app.route('/create')
def create_recipe():
    if "user_id" not in session:
        return redirect('/logout')
    return render_template('create_recipe.html')

@app.route('/create_process', methods=['POST'])
def create_process():
    if 'user_id' not in session:
        return redirect('/logout')
    if not recipe.Recipe.validate_recipe(request.form):
        return redirect("/create")
    data = {
        'user_id': session['user_id'],
        'name': request.form['name'],
        'description': request.form['description'],
        'instruction': request.form['instruction'],
        'date_made': request.form['date_made'],
        'under': int(request.form['under'])
    }
    recipe.Recipe.save_recipe(data)
    return redirect('/dashboard')

@app.route("/edit/<int:id>")
def edit(id):
    if "user_id" not in session:
        return redirect('/logout')
    return render_template("edit_recipe.html",recipe_id=id)

@app.route("/edit_process/<int:id>",methods=['POST'])
def edit_process(id):
    if 'user_id' not in session:
        return redirect('/logout')
    if not recipe.Recipe.validate_recipe(request.form):
        return redirect(f"/edit/{id}")
    data = {
        'id':id,
        'name':request.form['name'],
        'description':request.form['description'],
        'instruction':request.form['instruction'],
        'date_made':request.form['date_made'],
        'under':int(request.form['under'])
    }
    print('----------------------')
    print(data)
    recipe.Recipe.edit_recipe(data)
    return redirect('/dashboard')

@app.route("/delete/<int:id>")
def delete(id):
    if "user_id" not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    recipe.Recipe.delete(data)
    return redirect('/dashboard')
