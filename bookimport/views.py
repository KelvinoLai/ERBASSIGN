import csv
from django.shortcuts import render
from django.http import HttpResponse
from .models import book, AdditionalAuthor


def index(request):
    show = request.GET.get("show", "books")
    message = ""
    books = book.objects.all()
    additional_authors = AdditionalAuthor.objects.all()
    joined_books = []
    # Prepare joined data for display and export
    for b in books:
        aa = AdditionalAuthor.objects.filter(reference=b.reference).first()
        joined_books.append(
            {
                "reference": b.reference,
                "title": b.title,
                "author": b.author,
                "author2": aa.author2 if aa else "",
                "author3": aa.author3 if aa else "",
                "author4": aa.author4 if aa else "",
                "author5": aa.author5 if aa else "",
                "author6": aa.author6 if aa else "",
                "author7": aa.author7 if aa else "",
                "author8": aa.author8 if aa else "",
                "author9": aa.author9 if aa else "",
                "author10": aa.author10 if aa else "",
                "publisher": b.publisher,
                "year": b.year,
                "series": b.series,
                "description": b.description,
                "category": b.category,
                "notes": b.notes,
                "isbn": b.isbn,
                "price": b.price,
            }
        )

    if request.method == "POST":
        action = request.POST.get("action")
        if action == "import_books":
            csv_file = request.FILES.get("csv_file")
            if not csv_file:
                message = "No file selected."
            else:
                decoded = csv_file.read().decode("utf-8").splitlines()
                COLUMN_MAP = {
                    "著者1": "author",
                    "書刊名": "title",
                    "出版者": "publisher",
                    "出版年份": "year",
                    "叢書名": "series",
                    "著錄": "description",
                    "類別": "category",
                    "附註": "notes",
                    "國際標準書號": "isbn",
                    "定價": "price",
                    "參考編號": "reference",
                }
                reader = csv.DictReader(decoded)
                count = 0
                for row in reader:
                    book_data = {}
                    for cn_col, en_col in COLUMN_MAP.items():
                        book_data[en_col] = row.get(cn_col, "")
                    try:
                        book_data["year"] = int(float(book_data.get("year", 0)))
                    except Exception:
                        book_data["year"] = 0
                    price_str = (
                        book_data.get("price", "")
                        .replace("$", "")
                        .replace("CNY", "")
                        .replace("USD", "")
                        .replace(";", "")
                        .strip()
                    )
                    try:
                        book_data["price"] = float(price_str) if price_str else 0
                    except Exception:
                        book_data["price"] = 0
                    book.objects.create(**book_data)
                    count += 1
                message = f"Imported {count} books."
                books = book.objects.all()

        elif action == "import_authors":
            csv_file = request.FILES.get("csv_file")
            if not csv_file:
                message = "No file selected."
            else:
                decoded = csv_file.read().decode("utf-8").splitlines()
                COLUMN_MAP = {
                    "參考編號": "reference",
                    "著者2": "author2",
                    "著者3": "author3",
                    "著者4": "author4",
                    "著者5": "author5",
                    "著者6": "author6",
                    "著者7": "author7",
                    "著者8": "author8",
                    "著者9": "author9",
                    "著者10": "author10",
                }
                reader = csv.DictReader(decoded)
                count = 0
                for row in reader:
                    aa_data = {}
                    for cn_col, en_col in COLUMN_MAP.items():
                        aa_data[en_col] = row.get(cn_col, "")
                    if aa_data.get("reference"):
                        AdditionalAuthor.objects.update_or_create(
                            reference=aa_data["reference"], defaults=aa_data
                        )
                        count += 1
                message = f"Imported {count} additional author records."
                additional_authors = AdditionalAuthor.objects.all()

        elif action == "clear":
            book.objects.all().delete()
            AdditionalAuthor.objects.all().delete()
            message = "Database cleared."
            books = []
            additional_authors = []
            joined_books = []

        elif action == "export_books":
            response = HttpResponse(content_type="text/csv")
            response["Content-Disposition"] = 'attachment; filename="books.csv"'
            writer = csv.writer(response)
            writer.writerow(
                [
                    "title",
                    "author",
                    "publisher",
                    "year",
                    "series",
                    "description",
                    "category",
                    "notes",
                    "isbn",
                    "price",
                    "reference",
                ]
            )
            for b in book.objects.all():
                writer.writerow(
                    [
                        b.title,
                        b.author,
                        b.publisher,
                        b.year,
                        b.series,
                        b.description,
                        b.category,
                        b.notes,
                        b.isbn,
                        b.price,
                        b.reference,
                    ]
                )
            return response

        elif action == "export_authors":
            response = HttpResponse(content_type="text/csv")
            response["Content-Disposition"] = 'attachment; filename="authors.csv"'
            writer = csv.writer(response)
            writer.writerow(
                [
                    "reference",
                    "title",
                    "author",
                    "author2",
                    "author3",
                    "author4",
                    "author5",
                    "author6",
                    "author7",
                    "author8",
                    "author9",
                    "author10",
                ]
            )
            for aa in AdditionalAuthor.objects.all():
                # Find the book for title/author
                b = book.objects.filter(reference=aa.reference).first()
                writer.writerow(
                    [
                        aa.reference,
                        b.title if b else "",
                        b.author if b else "",
                        aa.author2,
                        aa.author3,
                        aa.author4,
                        aa.author5,
                        aa.author6,
                        aa.author7,
                        aa.author8,
                        aa.author9,
                        aa.author10,
                    ]
                )
            return response

        elif action == "export_joined":
            response = HttpResponse(content_type="text/csv")
            response["Content-Disposition"] = 'attachment; filename="joined_books.csv"'
            writer = csv.writer(response)
            writer.writerow(
                [
                    "title",
                    "author",
                    "author2",
                    "author3",
                    "author4",
                    "author5",
                    "author6",
                    "author7",
                    "author8",
                    "author9",
                    "author10",
                    "publisher",
                    "year",
                    "series",
                    "description",
                    "category",
                    "notes",
                    "isbn",
                    "price",
                    "reference",
                ]
            )
            for row in joined_books:
                writer.writerow(
                    [
                        row["title"],
                        row["author"],
                        row["author2"],
                        row["author3"],
                        row["author4"],
                        row["author5"],
                        row["author6"],
                        row["author7"],
                        row["author8"],
                        row["author9"],
                        row["author10"],
                        row["publisher"],
                        row["year"],
                        row["series"],
                        row["description"],
                        row["category"],
                        row["notes"],
                        row["isbn"],
                        row["price"],
                        row["reference"],
                    ]
                )
            return response

    return render(
        request,
        "index.html",
        {
            "books": books,
            "additional_authors": additional_authors,
            "joined_books": joined_books,
            "message": message,
            "show": show,
        },
    )
