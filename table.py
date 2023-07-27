import xlsxwriter
import io

def writer(data):
    output = io.BytesIO()
    book = xlsxwriter.Workbook(output, {'in_memory':True})
    page = book.add_worksheet()

    page.set_column("A:A", 30)
    page.set_column("B:B", 30)
    page.set_column("C:C", 30)
    page.set_column("D:D", 30)
    page.set_column("E:E", 50)
    page.set_column("F:F", 60)


    page.write_row(
       0, 0, ["Name", "Category", "District", "Number", "Address_full", "Site"]
    )
    for row, obj in enumerate(data):
        row_obj = [
            obj.get("name"),
            obj.get("category"),
            obj.get("district"),
            obj.get("number"),
            obj.get("address_full"),
            obj.get("site"),

        ]
        page.write_row(row+1, 0, row_obj)

    book.close()
    output.seek(0)
    with open("data.xlsx", "wb") as file:
        file.write(output.getbuffer())
