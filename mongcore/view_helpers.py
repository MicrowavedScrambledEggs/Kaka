import csv
from django.http import StreamingHttpResponse


class Echo(object):
    """Copied from docs.djangoproject.com/en/1.8/howto/outputting-csv/

    An object that implements just the write method of the file-like
    interface.
    """
    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value


def write_stream_response(rows, experi_name):
    writer = csv.writer(Echo())
    reader = csv.reader(rows)
    # Write query results to csv response
    response = StreamingHttpResponse((writer.writerow(r) for r in reader),
                                     content_type="text/csv")
    content = 'attachment; filename="' + experi_name + '.csv"'
    response['Content-Disposition'] = content
    return response