import json

from fastapi import FastAPI, Request, Depends, HTTPException, status, Body
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

app = FastAPI()
oauth_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.get("/ping")
def home():
    return "Pong"

#@app.post(path="/token")
def login(form_data: OAuth2PasswordRequestForm):
    print(form_data)
    with open("userdb.json", "r") as json_file:
        json_data = json.load(json_file)
        print(json_data)
    if json_data:
        password = json_data.get(form_data.username)
        print(password)
        if not password:
            print("Wrong Username or Password. Re-enter")
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Incorrect Username or Password")
    return {"access_token": form_data.username, "token_type": "bearer"}


@app.get("/spend/history")
def spend_history(token: str):
    print(token)
    with open("spendhist.json", "r") as spend_hist:
        spend_hist_data = json.load(spend_hist)
        if not spend_hist_data.get(token):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username not found is the spend history DB")
    return {
        "username": token,
        "spend_hist": spend_hist_data[token]
    }


@app.get("creditcard/history")
def credit_history(token: str):
    print(token)
    with open("credithist.json", "r") as credit_hist:
        credit_hist_data = json.load(credit_hist)
        if not credit_hist_data.get(token):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username not found is the credit history DB")
    return {
        "username": token,
        "credit_hist": credit_hist_data[token]
    }


@app.post("/transfer_money")
def transfer_money(token: str, destination_user: str = Body(...), amount_to_transfer: float = Body(...)):

    print(token)
    print(destination_user)
    print(amount_to_transfer)

    with open("userbalance.json", "r") as user_balance_file:
        user_balance_data = json.load(user_balance_file)
        curr_user_bal = user_balance_data.get(token)["curr_balance"]
        print(f"Current user balance is {curr_user_bal}")
        dest_user = user_balance_data.get(destination_user)
        if not dest_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Destination User is not present in the DB, Cannot transfer money")
        dest_user_bal = dest_user['curr_balance']
        print(f"Destination User Balance = {dest_user_bal}")
        if curr_user_bal - amount_to_transfer < 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Amount to transfer is greater than account balance. Cannot transfer money")
    user_balance_data[token]["curr_balance"] -= amount_to_transfer
    user_balance_data[destination_user]["curr_balance"] += amount_to_transfer
    with open("userbalance.json", "w") as user_bal_write:
        json.dump(user_balance_data, user_bal_write)
    return {
        "username": token,
        "message": f"Money {amount_to_transfer} successfully Transferred"
    }


@app.get("/userbalance")
def get_user_balance(token: str):
    with open("userbalance.json", "r") as user_file:
        user_balance = json.load(user_file)
    if not user_balance.get(token):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username not present in the userbalance DB")
    return {
        "username": token,
        "current_balance": user_balance.get(token)["curr_balance"]
    }
