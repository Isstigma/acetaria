from __future__ import annotations

import random
from datetime import datetime, timedelta, timezone
from app.core.db import get_session

HSR_SLUG = "hsr"
HSR_NAME = "Honkai: Star Rail"


def _cdn(path: str) -> str:
    return f"https://cdn.acetaria.example/{path}".replace("//", "//")


async def _ensure_indexes(db) -> None: pass
    # await db.runs.create_index([("publishedAt", -1)])
    # await db.leaderboard_entries.create_index([("gameSlug", 1), ("modeSlug", 1), ("cycles", 1), ("limStd", 1)])
    # await db.leaderboard_entries.create_index([("gameSlug", 1), ("modeSlug", 1), ("timeMs", 1), ("limStd", 1)])
    # await db.team_entries.create_index([("entryId", 1)])


async def ensure_seeded() -> None:
    db = get_session()
    await _ensure_indexes(db)
    await seed_minimum(db)

    await _ensure_indexes(db)
    if await db.games.count_documents({}) > 0:
        return
    await seed(db)


async def seed_minimum(db) -> None:
    """Idempotently upsert minimum docs needed for the frontend to work."""
    now = datetime.now(timezone.utc)

    await db.games.update_one(
        {"slug": HSR_SLUG},
        {"$set": {"slug": HSR_SLUG, "name": HSR_NAME}},
        upsert=True,
    )

    modes = [
        {"gameSlug": HSR_SLUG, "modeSlug": "memory-of-chaos", "modeName": "Memory of Chaos", "playMetricType": "cycles", "isLatest": True},
        {"gameSlug": HSR_SLUG, "modeSlug": "pure-fiction", "modeName": "Pure Fiction", "playMetricType": "time", "isLatest": False},
        {"gameSlug": HSR_SLUG, "modeSlug": "apocalyptic-shadow", "modeName": "Apocalyptic Shadow", "playMetricType": "cycles", "isLatest": False},
        {"gameSlug": HSR_SLUG, "modeSlug": "anomaly-arbitration", "modeName": "Anomaly Arbitration", "playMetricType": "time", "isLatest": False},
    ]
    for m in modes:
        await db.modes.update_one(
            {"gameSlug": HSR_SLUG, "modeSlug": m["modeSlug"]},
            {"$set": m},
            upsert=True,
        )

    featured_run = {
        "runId": "run_featured_001",
        "gameSlug": HSR_SLUG,
        "gameName": HSR_NAME,
        "modeSlug": "memory-of-chaos",
        "modeName": "Memory of Chaos",
        "title": "How To Take Castorice Passive To The Next Level | RMC Solo DPS 0-Cycle Mafma | New MoC 3.1",
        "place": 1,
        "metric": {"type": "cycles", "cycles": 0},
        "playerName": "Herrscher of Sentience (识之律者)",
        "publishedAt": now - timedelta(minutes=42),
        "video": {
            "platform": "youtube",
            "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "title": "RMC Solo DPS 0-Cycle (seed)",
            "durationMs": 612_000,
            "thumbnailUrl": _cdn("thumbnails/featured_001.jpg"),
        },
    }
    await db.runs.update_one({"runId": featured_run["runId"]}, {"$set": featured_run}, upsert=True)

    # If characters are missing, seed the full dataset
    if await db.characters.count_documents({"gameSlug": HSR_SLUG}) == 0:
        await seed(db)

async def seed(db: AsyncIOMotorDatabase) -> None:
    now = datetime.now(timezone.utc)

    await db.games.insert_many([{"slug": HSR_SLUG, "name": HSR_NAME}])

    modes = [
        {"gameSlug": HSR_SLUG, "modeSlug": "memory-of-chaos", "modeName": "Memory of Chaos", "playMetricType": "cycles", "isLatest": True},
        {"gameSlug": HSR_SLUG, "modeSlug": "pure-fiction", "modeName": "Pure Fiction", "playMetricType": "time", "isLatest": False},
        {"gameSlug": HSR_SLUG, "modeSlug": "apocalyptic-shadow", "modeName": "Apocalyptic Shadow", "playMetricType": "cycles", "isLatest": False},
        {"gameSlug": HSR_SLUG, "modeSlug": "anomaly-arbitration", "modeName": "Anomaly Arbitration", "playMetricType": "time", "isLatest": False},
    ]
    await db.modes.insert_many(modes)

    character_names = [
        "Acheron", "Kafka", "Jingliu", "Firefly", "Seele",
        "Dan Heng • Imbibitor Lunae", "Ruan Mei", "Sparkle", "Fu Xuan", "Blade",
        "Topaz", "Black Swan", "Bronya", "Himeko", "Welt",
        "Silver Wolf", "Luocha", "Huohuo", "Robin", "Aventurine",
        "Boothill", "Argenti", "Dr. Ratio", "Sunday", "Feixiao",
    ]
    characters = []
    for i, name in enumerate(character_names, start=1):
        cid = f"c_{i:03d}"
        characters.append({"id": cid, "gameSlug": HSR_SLUG, "name": name, "portraitUrl": _cdn(f"hsr/portraits/{cid}.png")})
    await db.characters.insert_many(characters)

    random.seed(7)

    def make_player(i: int) -> dict:
        return {"displayName": f"Player{i:02d}"}

    leaderboard_entries = []

    cycles_modes = ["memory-of-chaos", "apocalyptic-shadow"]
    idx = 0
    for mode_slug in cycles_modes:
        for i in range(12):
            c = characters[(idx + i) % len(characters)]
            leaderboard_entries.append(
                {
                    "entryId": f"le_{HSR_SLUG}_{mode_slug}_cycles_{i+1:03d}",
                    "gameSlug": HSR_SLUG,
                    "modeSlug": mode_slug,
                    "character": {"id": c["id"], "name": c["name"], "portraitUrl": c["portraitUrl"]},
                    "limStd": random.choice([0, 1, 2, 3, 4, 5]),
                    "cycles": random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]),
                    "player": make_player(idx + i + 1),
                    "createdAt": now - timedelta(days=random.randint(0, 60)),
                }
            )
        idx += 12

    time_modes = ["pure-fiction", "anomaly-arbitration"]
    for mode_slug in time_modes:
        for i in range(12):
            c = characters[(idx + i + 7) % len(characters)]
            leaderboard_entries.append(
                {
                    "entryId": f"le_{HSR_SLUG}_{mode_slug}_time_{i+1:03d}",
                    "gameSlug": HSR_SLUG,
                    "modeSlug": mode_slug,
                    "character": {"id": c["id"], "name": c["name"], "portraitUrl": c["portraitUrl"]},
                    "limStd": random.choice([0, 1, 2, 3, 4, 5]),
                    "timeMs": random.choice([55_000, 61_500, 72_300, 83_120, 95_450, 110_000, 133_333, 145_250]),
                    "player": make_player(idx + i + 1),
                    "createdAt": now - timedelta(days=random.randint(0, 60)),
                }
            )
        idx += 12

    await db.leaderboard_entries.insert_many(leaderboard_entries)

    featured_entry = leaderboard_entries[0]
    featured_entry_id = featured_entry["entryId"]

    def team_of4(offset: int) -> list[dict]:
        return [{"id": characters[(offset + j) % len(characters)]["id"], "portraitUrl": characters[(offset + j) % len(characters)]["portraitUrl"]} for j in range(4)]

    mixed_videos = [
        {"platform": "youtube", "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ", "title": "HSR 0-Cycle Showcase", "durationMs": 182_000, "thumbnailUrl": _cdn("thumbnails/youtube_001.jpg")},
        {"platform": "bilibili", "url": "https://www.bilibili.com/video/BV1xx411c7mD", "title": "HSR Team Tech (Bilibili)", "durationMs": 245_500, "thumbnailUrl": _cdn("thumbnails/bilibili_001.jpg")},
        {"platform": "twitch", "url": "https://www.twitch.tv/videos/1234567890", "title": "Live Run VOD (Twitch)", "durationMs": 3_600_000, "thumbnailUrl": _cdn("thumbnails/twitch_001.jpg")},
    ]

    team_entries = []
    for vid_idx, video in enumerate(mixed_videos, start=1):
        team_entries.append(
            {
                "teamEntryId": f"te_{featured_entry_id}_{vid_idx:02d}",
                "entryId": featured_entry_id,
                "gameSlug": HSR_SLUG,
                "modeSlug": featured_entry["modeSlug"],
                "team": team_of4(offset=vid_idx * 3),
                "limStd": random.choice([0, 1, 2, 3]),
                "cycles": max(0, int(featured_entry.get("cycles", 2)) + random.choice([0, 0, 1])),
                "player": {"displayName": f"TeamRunner{vid_idx:02d}"},
                "video": video,
                "createdAt": now - timedelta(days=random.randint(0, 30)),
            }
        )
    await db.team_entries.insert_many(team_entries)

    featured_run = {
        "runId": "run_featured_001",
        "gameSlug": HSR_SLUG,
        "gameName": HSR_NAME,
        "modeSlug": "memory-of-chaos",
        "modeName": "Memory of Chaos",
        "title": "How To Take Castorice Passive To The Next Level | RMC Solo DPS 0-Cycle Mafma | New MoC 3.1",
        "place": 1,
        "metric": {"type": "cycles", "cycles": 0},
        "playerName": "Herrscher of Sentience (识之律者)",
        "publishedAt": now - timedelta(minutes=42),
        "video": {
            "platform": "youtube",
            "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "title": "RMC Solo DPS 0-Cycle (seed)",
            "durationMs": 612_000,
            "thumbnailUrl": _cdn("thumbnails/featured_001.jpg"),
        },
    }
    # NOTE: we also seed a few extra runs for later development.
    other_runs = []
    for i in range(2, 7):
        m = random.choice(modes)
        metric = {"type": m["playMetricType"]}
        if metric["type"] == "cycles":
            metric["cycles"] = random.choice([0, 1, 2, 3, 4, 5])
        else:
            metric["timeMs"] = random.choice([49_500, 55_000, 61_500, 72_300, 83_120, 95_450])
        other_runs.append(
            {
                "runId": f"run_{i:03d}",
                "gameSlug": HSR_SLUG,
                "gameName": HSR_NAME,
                "modeSlug": m["modeSlug"],
                "modeName": m["modeName"],
                "title": random.choice(["Route Optimization", "Consistency Run", "Low Investment Run"]),
                "place": random.randint(2, 50),
                "metric": metric,
                "playerName": f"Runner{i:02d}",
                "publishedAt": now - timedelta(minutes=random.randint(60, 360)),
                "video": random.choice(mixed_videos),
            }
        )
    await db.runs.insert_many([featured_run, *other_runs])


async def _amain():
    db = get_session()
    await _ensure_indexes(db)
    await seed(db)


def main():
    import asyncio
    asyncio.run(_amain())


if __name__ == "__main__":
    main()
