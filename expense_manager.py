import numpy as np

friends = ["James", "Harish", "Kamal", "Santhosh"]

expense_matrix = np.zeros((len(friends), len(friends)))

expense_history = []


def add_expense(payer, beneficiaries, amount):

    payer_idx = friends.index(payer)

    share = amount / len(beneficiaries)

    for person in beneficiaries:
        idx = friends.index(person)
        expense_matrix[payer_idx][idx] += share

    expense_history.append({
        "payer": payer,
        "amount": amount,
        "beneficiaries": beneficiaries
    })


def add_custom_expense(payer, splits):

    payer_idx = friends.index(payer)

    for person, share in splits.items():

        idx = friends.index(person)

        expense_matrix[payer_idx][idx] += share

    expense_history.append({
        "payer": payer,
        "amount": sum(splits.values()),
        "beneficiaries": list(splits.keys())
    })


def calculate_balance():

    total_paid = np.sum(expense_matrix, axis=1)
    total_owed = np.sum(expense_matrix, axis=0)

    net = total_paid - total_owed

    result = {}

    for i, friend in enumerate(friends):

        if net[i] > 0:
            result[friend] = f"Should Receive {net[i]:.2f}"

        elif net[i] < 0:
            result[friend] = f"Owes {-net[i]:.2f}"

        else:
            result[friend] = "Settled"

    return result


def suggest_transactions():

    settlements = calculate_balance()

    creditors = []
    debtors = []

    for name, status in settlements.items():

        if "Receive" in status:
            amount = float(status.split()[-1])
            creditors.append((name, amount))

        if "Owes" in status:
            amount = float(status.split()[-1])
            debtors.append((name, amount))

    transactions = []

    while debtors and creditors:

        debtor, debt = debtors.pop(0)
        creditor, credit = creditors.pop(0)

        payment = min(debt, credit)

        transactions.append({
            "debtor": debtor,
            "creditor": creditor,
            "amount": payment
        })

        debt -= payment
        credit -= payment

        if debt > 0:
            debtors.insert(0, (debtor, debt))

        if credit > 0:
            creditors.insert(0, (creditor, credit))

    return transactions


def get_expense_history():
    return expense_history