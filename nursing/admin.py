from django.contrib import admin
from .models import UserApplication


# Adding libraries to export the data
import io
import pandas as pd
from django.http import HttpResponse

# Adding libraries for pdf creation
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from django.http import FileResponse


# Creating a custom admin action that will appear as an option on the admin page. When the admin selects the UserApplications, Django should execute this function.
class UserApplicationAdmin(admin.ModelAdmin):
    def export_selected_objects(self, request, queryset):
        # Create a DataFrame from the queryset
        user_dataframe = pd.DataFrame.from_records(queryset.values())

        # Create an HTTPResponse object with the xls content type
        response = HttpResponse(content_type="application/vnd.ms-excel")

        # Set the response content disposition to an attachment, with an appropriate filename.
        response["Content-Disposition"] = "attachment; filename = applications.xlsx"

        # Write the DataFrame to an Excel file, directly to the HttpResponse object.
        user_dataframe.to_excel(response, index=False)

        # Return the HttpResponse object.
        return response

    def export_translated_objects(self, request, queryset):
        # Create a DataFrame from the queryset, but this time we include 'about_me_translated'
        user_dataframe = pd.DataFrame.from_records(
            queryset.values("name", "last_name", "age", "email", "about_me_translated")
        )

        # Create an HTTPResponse object with the xls content type
        response = HttpResponse(content_type="application/vnd.ms-excel")

        # Set the response content disposition to an attachment, with an appropriate filename.
        response[
            "Content-Disposition"
        ] = "attachment; filename = applications_translated.xlsx"

        # Write the DataFrame to an Excel file, directly to the HttpResponse object.
        user_dataframe.to_excel(response, index=False)

        # Return the HttpResponse object.
        return response

    def export_translated_pdf(self, request, queryset):
        # Create a file-like buffer to receive PDF data.
        buffer = io.BytesIO()

        # Create the PDF object, using the buffer as its "file."
        doc = SimpleDocTemplate(buffer, pagesize=letter)

        # Fetch the text style
        styles = getSampleStyleSheet()
        story = []

        for obj in queryset:
            # For every field in our object, we'll write a line in our PDF
            fields = [
                f"Name: {obj.name}",
                f"Last name: {obj.last_name}",
                f"Age: {obj.age}",
                f"Email: {obj.email}",
                f"About Me (translated): {obj.about_me_translated}",
            ]
            for field in fields:
                p = Paragraph(field, styles["Normal"])
                story.append(p)
                story.append(Spacer(1, 12))

            # Add extra space between UserApplications
            story.append(Spacer(1, 24))

        # Build the PDF
        doc.build(story)

        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename="translated_data.pdf")

    # We need to give our action a short description which will be displayed in the admin interface
    export_selected_objects.short_description = "Export selected UserApplications"

    export_translated_objects.short_description = (
        "Export selected UserApplications (translated)"
    )

    export_translated_pdf.short_description = (
        "Export selected UserApplications to PDF (translated)"
    )

    # Register our action
    actions = [
        export_selected_objects,
        export_translated_objects,
        export_translated_pdf,
    ]


# Registering the UserApplication model with the custom UserApplicationAdmin
admin.site.register(UserApplication, UserApplicationAdmin)
