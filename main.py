from email.policy import HTTP
from fastapi import FastAPI, HTTPException
from uuid import UUID
from typing import List
from models import User, Gender, Product, Cart


app = FastAPI()

db = {
    'user': [
        User(
            id = 10,
            first_name = "Jamila",
            last_name = "Ahmed",
            gender = Gender.female,
            Cart = None
        ),
        User(
            id = 5,
            first_name = "Alex",
            last_name = "Jones",
            gender = Gender.male,
            Cart = None
        ),
    ],
    'products': [
        Product(
            id = 2,
            price = 10.2,
            name = "Pao de queijo"
        ),
        Product(
            id = 1,
            price = 20.0,
            name = "Cafe de vinte conto"
        ),
        Product(
            id = 8,
            price = 15,
            name = "Iogurte"
        ),
    ]
}

# Get de todos os usuários do db
@app.get("/users")
async def fetch_users():
    return db["user"]


# Get de um usuário
@app.get("/user/{user_id}/")
def read_items(user_id: str):
    vef = 0
    for u in db['user']:
        print(u.id)
        if u.id == UUID(user_id):
            vef = 0
            return u
        
        else:
            vef = 1
    
    if vef == 1:
        raise HTTPException(status_code = 404, detail = "User not found")

# Get de um produto
@app.get("/produto/{produto_id}/")
def read_items(carrinho_id: int):
    vef = 0
    for products in db['products']:
        print(products.id)
        if products.id == carrinho_id:
            vef = 0
            return products
        
        else:
            vef = 1
    
    if vef == 1:
        raise HTTPException(status_code = 404, detail = "Item not found")

# Post de um usuário
@app.post("/api/v1/users")
async def register_user(user: User):
    db["user"].append(user)
    return {"id": user.id}

@app.post("/api/v1/cart/{user_id}/{product_name}")
async def addItems(user_id: str, product_name: str):
    selUser = None
    selProduct = None
    for user in db["user"]:
        if user.id == UUID(user_id):
            selUser = user
    if(selUser == None):
        return "Nenhum Usuario Encontrado."
    else:
        for product in db["products"]:
            if(product.name == product_name):
                selProduct = product
                
        if(selProduct == None):
            return "Nenhum Produto Encontrado"
        else:
            if(selUser.cart == None):
                newCart = Cart(
                    id = 1,
                    products = [selProduct]
                )
                selUser.cart = newCart
            else:
                selUser.cart.products.append(selProduct)

            return selUser

#Get do Carrinho
@app.get("/carrinho/{user_Id}")
def getCart(user_id: int):
    selUser = None

    for user in db["user"]:
        if user.id == user_id:
            selUser = user
    if(selUser == None):
        return "Nenhum Usuario Encontrado."
    else:
        if(selUser.cart == None):
            return "O usuário não contem nenhum produto em seu carrinho"
        else:
            return selUser.cart
    

#Delete Produto do Carrinho
@app.delete("/api/v1/cart/{user_id}/{product_id}")
async def deleteFromCart(user_id: str, product_id: str):
    selUser = None
    selProduct = None
    for user in db["user"]:
        if(user.id == UUID(user_id)):
            selUser = user
    if(selUser == None):
        return "Nenhum Usuario Encontrado."
    else:
        if(selUser.cart == None):
                return "Não existe nenhum produto neste carrinho"
        
        else:
            for product in selUser.cart.products:
                if(product.id == UUID(product_id)):
                    selProduct = product
                
            if(selProduct == None):
                return "Nenhum Produto Encontrado Neste Carrinho Com esse ID"
            
            else:
                for e in selUser.cart.products:
                    if(UUID(product_id) == e.id):
                        selUser.cart.products.remove(e)

                return "Produto Apagado"



# Delete de um usuário
@app.delete("/api/v1/users/{user_id}")
async def delete_user(user_id: UUID):
    for user in db["user"]:
        if user.id == user_id:
            db["user"].remove(user)
            return 
    raise HTTPException (
        status_code = 404,
        detail = f"user with id: {user_id} does not exists"
    )