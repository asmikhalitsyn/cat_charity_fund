from datetime import datetime
from typing import List, Union

from app.models import CharityProject, Donation


def close_donation_for_obj(obj_in: Union[CharityProject, Donation]):
    obj_in.fully_invested = True
    obj_in.close_date = datetime.now()
    return obj_in


def investing_process(
        obj_in: Union[CharityProject, Donation],
        model_add: List[Union[CharityProject, Donation]],
) -> List[Union[CharityProject, Donation]]:
    obj_in.invested_amount = obj_in.invested_amount or 0
    count = 0
    for balance in model_add:
        donation = min(
            balance.full_amount - balance.invested_amount,
            obj_in.full_amount - obj_in.invested_amount
        )
        for project in [balance, obj_in]:
            project.invested_amount += donation
            if project.full_amount == project.invested_amount:
                close_donation_for_obj(project)
        count += 1
    return model_add[:count]
