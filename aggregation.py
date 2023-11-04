from typing import List
from datetime import datetime, timedelta

from db import collection


async def aggregate_payments(
    dt_from: str, dt_upto: str, group_type: str
) -> dict[str, List[int] | List[str]]:

    dtfrom = datetime.fromisoformat(dt_from)
    dtupto = datetime.fromisoformat(dt_upto) + timedelta(milliseconds=1)

    dataset, labels = [], []

    fill_stage = {
        "$densify": {
            "field": "dt",
            "range": {
                "step": 1,
                "unit": group_type,
                "bounds": [dtfrom, dtupto],
            },
        }
    }

    match_stage = {
        "$match": {
            "dt": {
                "$gte": dtfrom,
                "$lte": dtupto,
            },
        }
    }

    group_stage = {
        "$group": {
            "_id": {
                "year": {"$year": "$dt"},
                "month": {"$month": "$dt"},
                "day": {"$dayOfMonth": "$dt"},
                "hour": {"$hour": "$dt"},
            },
            "value": {"$sum": "$value"},
        }
    }

    if group_type == "month":
        group_stage["$group"]["_id"].pop("day")
        group_stage["$group"]["_id"].pop("hour")
    elif group_type == "day":
        group_stage["$group"]["_id"].pop("hour")
    elif group_type == "hour":
        pass

    sort_stage = {
        "$sort": {
            "_id": 1,
        }
    }

    async for doc in collection.aggregate(
        [fill_stage, match_stage, group_stage, sort_stage]
    ):
        doc_dt: dict = doc["_id"]
        dt = datetime(
            doc_dt.get("year"),
            doc_dt.get("month"),
            doc_dt.get("day", 1),
            doc_dt.get("hour", 0),
        )

        dataset.append(doc["value"])
        labels.append(dt.isoformat())

    return {"dataset": dataset, "labels": labels}
