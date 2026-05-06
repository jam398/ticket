from sqlmodel import Session

from app.database import engine, init_db
from app.services.seed_data import seed_database


def main() -> None:
    init_db()
    with Session(engine) as session:
        tickets = seed_database(session)
    print(f"Seeded {len(tickets)} tickets.")


if __name__ == "__main__":
    main()
