import datetime

from app.models import ProjectDonationBase

DEFAULT_INVESTED_AMOUNT = 0


def invest(
    target: ProjectDonationBase, sources: list[ProjectDonationBase]
) -> list[ProjectDonationBase]:
    updated = []
    for investment in sources:
        if target.invested_amount is None:
            target.invested_amount = DEFAULT_INVESTED_AMOUNT
        amendment = min(
            investment.full_amount - investment.invested_amount,
            target.full_amount - target.invested_amount,
        )

        for instance in (investment, target):
            instance.invested_amount += amendment
            if instance.invested_amount == instance.full_amount:
                instance.fully_invested = True
                instance.close_date = datetime.datetime.now()

        updated.append(investment)
        if target.fully_invested:
            break
    updated.append(target)
    return updated
