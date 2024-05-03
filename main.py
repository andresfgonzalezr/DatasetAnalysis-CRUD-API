from fastapi import FastAPI, Depends
from database.crud import CRUD, get_gpt
from database.models import DataItems
from sqlalchemy.orm import Session


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()


# Set up a route POST that allows to create new elements in the DataBase and give back the data of the created elements with the estructure of the DataItems
@app.post("/items/create", response_model=DataItems)
def create_items_route(item_data: DataItems, db: Session = Depends(get_db)):
    CRUD.create(item_data, db)
    return "created row"


@app.get("/items/read/{id_df}")
def read_item_by_id(id_df: int, db: Session = Depends(get_db)):
    data = CRUD.read_by_id(id_df, db)
    return {"respose": data}


@app.get("/items/read")
def read_all_items(db: Session = Depends(get_db)):
    read = CRUD.read(db)
    return {read}


# Set up a route PUT in order to update a row from the DataBase, using the id in order to know which row it has to be update and using a dictionary to complete the information
@app.put("/items/{item_id}/update", response_model=DataItems)
def update_item(item_id: int, item_data: DataItems, db: Session = Depends(get_db)):
    return CRUD.update_data(item_id, item_data, db)


# Set up a route DELETE in order to delete a row from the project.
@app.delete("/items/{item_id}/delete", response_model=DataItems)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    return CRUD.delete_data(item_id, db)


@app.post("/items/gpt")
def use_gpt(prompt):
    return get_gpt(prompt)


# if __name__ == "__main__":
    # clean_data()
