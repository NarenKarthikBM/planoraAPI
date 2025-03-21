import csv
import io

def csv_to_dict(csv_file):
    """
    Convert a CSV file to a list of dictionaries.

    Args:
        csv_file (InMemoryUploadedFile or file object): CSV file uploaded by the user.

    Returns:
        list: List of dictionaries where keys are column headers and values are row values.
    """
    csv_file.seek(0)  # Ensure the file pointer is at the beginning
    decoded_file = io.StringIO(csv_file.read().decode("utf-8"))
    reader = csv.DictReader(decoded_file)
    return list(reader)


def dict_to_csv(data, fieldnames):
    """
    Convert a list of dictionaries to a CSV formatted string.

    Args:
        data (list): List of dictionaries to be converted.
        fieldnames (list): List of column headers.

    Returns:
        str: CSV formatted string.
    """
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data)
    return output.getvalue()


def get_event_import_csv_format():
    """
    Returns the required CSV format for bulk event import.

    Returns:
        list: List of column headers for CSV file.
    """
    return [
        "name",
        "scan_id",
        "description",
        "start_datetime",
        "end_datetime",
        "category",
        "tags",
        "type",
        "location",
        "latitude",
        "longitude",
        "status",
        "created_by",
    ]
