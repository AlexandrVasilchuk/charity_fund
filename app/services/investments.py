import datetime

from app.models import ProjectDonationBase


def invest(
    target: ProjectDonationBase, sources: list[ProjectDonationBase]
) -> list[ProjectDonationBase]:
    updated = []
    for investment in sources:
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
    return updated
