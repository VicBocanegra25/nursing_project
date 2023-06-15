from django.contrib import admin
from .models import UserApplication

# Adding libraries to export the data
import pandas as pd
from django.http import HttpResponse


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

    # We need to give our action a short description which will be displayed in the admin interface
    export_selected_objects.short_description = "Export selected UserApplications"

    # Register our action
    actions = [export_selected_objects]


# Registering the UserApplication model with the custom UserApplicationAdmin
admin.site.register(UserApplication, UserApplicationAdmin)
