from datetime import datetime
from typing import List, Union

from app.models import CharityProject, Donation, InvestmentDate


def close_donation_for_obj(obj_in: Union[CharityProject, Donation]):
    obj_in.fully_invested = True
    obj_in.close_date = datetime.now()
    return obj_in


def investing_process(
        target: Union[CharityProject, Donation],
        sources: List[Union[CharityProject, Donation]],
) -> List[InvestmentDate]:
    target.invested_amount = target.invested_amount or 0
    count = 0
    for source in sources:
        donation = min(
            source.full_amount - source.invested_amount,
            target.full_amount - target.invested_amount
        )
        for obj in [source, target]:
            obj.invested_amount += donation
            if obj.full_amount == obj.invested_amount:
                obj.close_date = datetime.now()
                obj.fully_invested = True
        count += 1
    return sources[:count]
