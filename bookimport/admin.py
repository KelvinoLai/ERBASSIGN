from django.contrib import admin


# Register your models here.
class bookAdmin(admin.ModelAdmin):
    "id",
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


list_filter = ("author", "publisher", "category")

# Filters to apply in the admin interface
list_editable = ("publisher", "series", "isbn" "price")
# Fields that can be edited directly in the list view
search_fields = ("author", "title", "publisher")
# Fields to search in the admin interface
list_per_page = 25  # Number of listings to display per page in the admin interface
ordering = ["-id"]
