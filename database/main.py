from fastapi import FastAPI, Depends
from cleaning_data import clean_data
from crud import CRUD, get_gpt
from models import DataItems


app = FastAPI()


# Set up a route POST that allows to create new elements in the DataBase and give back the data of the created elements with the estructure of the DataItems

@app.post("/items/create", response_model=DataItems)
def create_items_route(item_data: DataItems):
    CRUD.create(item_data)
    return "created row"


@app.get("/items/read/{id}")
def read_item_by_id(id: int):
    return {CRUD.read_by_id(id)}


@app.get("/items/read")
def read_all_items():
    read = CRUD.read()
    return {read}


# Set up a route PUT in order to update a row from the DataBase, using the id in order to know which row it has to be update and using a dictionary to complete the information
@app.put("/items/{item_id}/update", response_model=DataItems)
def update_item(item_id: int, item_data: DataItems):
    return CRUD.update_data(item_id, item_data)


# Set up a route DELETE in order to delete a row from the project.
@app.delete("/items/{item_id}/delete", response_model=DataItems)
def delete_item(item_id: int):
    return CRUD.delete_data(item_id)


@app.post("/items/gpt")
def use_gpt(prompt):
    return get_gpt(prompt)


if __name__ == "__main__":
    clean_data()
