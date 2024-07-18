from fastapi import FastAPI, Depends, HTTPException
from database.crud import create, read, read_by_id, update_data, delete_data, get_gpt
from utils.models import DataItems
from sqlalchemy.orm import Session
from database.database_ import SessionLocal
import logging


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()


# Set up a route POST that allows to create new elements in the DataBase and give back the data of the created elements with the estructure of the DataItems
@app.post("/create", response_model=DataItems)
def create_items_route(item_data: DataItems, db: Session = Depends(get_db)):
    data_dict = item_data.dict()
    new_data = create(data_dict, db)
    return new_data


@app.post("/read_user/{id_df}")
def read_item_by_id(id_df: int, db: Session = Depends(get_db)):
    logging.info(f"API called with id_df: {id_df}")
    data = read_by_id(id_df, db)
    return {"response": data}


@app.get("/read")
def read_all_items(db: Session = Depends(get_db)):
    read(db)
    return {"response": read(db)}


# Set up a route PUT in order to update a row from the DataBase, using the id in order to know which row it has to be update and using a dictionary to complete the information
@app.put("/update/{item_id}", response_model=DataItems)
def update_item(item_id: int, item_data: DataItems, db: Session = Depends(get_db)):
    return update_data(item_id, item_data, db)


# Set up a route DELETE in order to delete a row from the project.
@app.delete("/delete/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    delete_data(item_id, db)


@app.post("/gpt")
def use_gpt(input_prompt: str, db: Session = Depends(get_db)):
    try:
        get_gpt(input_prompt, db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# For using the gpt function introduce the prompt you want to use with the typo of request you want to apply into the database, this funcition will use the get_gpt function in order o process the prompt and apply the crud function that has the type of request you want to use
# run me with uvicorn...

# if __name__ == "__main__":
    # clean_data()

# if __name__ == '__main__':
    # import uvicorn
    # uvicorn.run(app)