from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from expense_manager import (
    add_expense,
    add_custom_expense,
    calculate_balance,
    suggest_transactions,
    get_expense_history,
    friends
)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):

    balances = calculate_balance()
    transactions = suggest_transactions()
    expenses = get_expense_history()

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "friends": friends,
            "balances": balances,
            "transactions": transactions,
            "expenses": expenses
        }
    )


@app.post("/add_expense")
def add_expense_route(
    payer: str = Form(...),
    amount: float = Form(...),
    beneficiaries: str = Form(None),
    split_type: str = Form(...),
    custom_split: str = Form(None)
):

    if split_type == "equal":

        people = beneficiaries.split(",")

        add_expense(payer, people, amount)

    else:

        splits = {}

        for item in custom_split.split(","):
            name, value = item.split(":")
            splits[name] = float(value)

        add_custom_expense(payer, splits)

    return RedirectResponse("/", status_code=303)