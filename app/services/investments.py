import datetime

from app.models import ProjectDonationBase


def invest(target: ProjectDonationBase, sources: list[ProjectDonationBase]):
    updated_investments = []
    for investment in sources:
        amendment = min(
            investment.full_amount - investment.invested_amount,
            target.full_amount,
        )
        target.invested_amount = amendment
        investment.invested_amount += amendment

        for instance in (investment, target):
            if instance.invested_amount == instance.full_amount:
                instance.fully_invested = True
                instance.close_date = datetime.datetime.now()
            updated_investments.append(instance)

        if target.fully_invested:
            return updated_investments
    return updated_investments
