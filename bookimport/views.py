import csv
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import book


def index(request):
    message = ""
    books = book.objects.all()
    if request.method == "POST":
        action = request.POST.get("action")
        if action == "import":
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
                    # Clean year
                    try:
                        book_data["year"] = int(float(book_data.get("year", 0)))
                    except Exception:
                        book_data["year"] = 0
                    # Clean price (remove $ and convert to float)
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
        elif action == "clear":
            book.objects.all().delete()
            message = "Database cleared."
            books = []
        elif action == "export":
            response = HttpResponse(content_type="text/csv")
            response["Content-Disposition"] = 'attachment; filename="books.csv"'
            writer = csv.writer(response)
            writer.writerow(
                [
                    "author",
                    "title",
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
                        b.author,
                        b.title,
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
    return render(request, "index.html", {"books": books, "message": message})
