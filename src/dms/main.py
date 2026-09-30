from src.dms.database.database import (
    add_document,
    get_documents,
)


def main():
    print("DMS started")
    add_document("Telekom Rechnung September")
    add_document("Telekom Rechnung August")
    add_document("O2 Rechnung April")
    print("Added document")
    print("Documents")
    documents = get_documents()

    for d in documents:
        print(f"{d.id}: {d.title}")


if __name__ == '__main__':
    main()
