from django.db.models import Sum

from expenses.models import Expense


def get_total_expenses() -> str:
    """Calculate the total amount of all recorded expenses."""

    total = Expense.objects.aggregate(
        total=Sum("amount")
    )["total"]

    total = total or 0

    return f"Total expenses: Rs. {total:.2f}"


def get_category_total(category: str) -> str:
    """Calculate the total expenses for a specified category."""

    total = Expense.objects.filter(
        category__iexact=category
    ).aggregate(
        total=Sum("amount")
    )["total"]

    if total is None:
        return f"No expenses found for category: {category}"

    return f"Total spending on {category}: Rs. {total:.2f}"


def get_highest_spending_category() -> str:
    """Find the expense category with the highest total spending."""

    result = (
        Expense.objects
        .values("category")
        .annotate(total=Sum("amount"))
        .order_by("-total", "category")
        .first()
    )

    if result is None:
        return "No expenses are available."

    return (
        f"Highest spending category: {result['category']}. "
        f"Total: Rs. {result['total']:.2f}"
    )