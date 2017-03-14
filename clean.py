import csv

def compare_same_table(row_a,row_b):
    if (row_a["fye"] < row_b["fye"]):
        return -1
    elif row_a["fye"] == row_b["fye"]:
        if row_a["standname"] < row_b["standname"]:
            return -1
        elif row_a["standname"] == row_b["standname"]:
            if row_a["totalcomp"] < row_b["totalcomp"]:
                return -1
            elif row_a["totalcomp"] == row_b["totalcomp"]:
                return 0
            else:
                return 1
        else:
            return 1
    else:
        return 1

def list_dup_rows(list_b):
    result = []
    i = 1
    current = 0
    while i < len(list_b):
        if compare_same_table(list_b[current], list_b[i]) == 0:
            if i - current == 1:
                result.append(list_b[current])
            result.append(list_b[i])
        else:
            current = i
        i += 1
    return result

def output_dup_rows():
    with open("duplicate_rows.csv",'w') as output_csv_file:
        with open("output.csv") as b:
            d_reader_b = csv.DictReader(b)
            list_b = []
            for i, row in enumerate(d_reader_b):
                list_b.append(row)
            
            # Prepare the output writer.
            d_writer = csv.DictWriter(output_csv_file, fieldnames=d_reader_b.fieldnames)
            d_writer.writeheader()
            d_writer.writerows(list_dup_rows(list_b))


def output_compare():
    with open("final_output.csv",'w') as output_csv_file:
        with open('input.csv') as a, open('output.csv') as b:
            d_reader_a = csv.DictReader(a)
            d_reader_b = csv.DictReader(b)
            list_a = []
            list_b = []
            for i, row in enumerate(d_reader_a):
                list_a.append(row)
            for i, row in enumerate(d_reader_b):
                list_b.append(row)

            # Prepare the output writer.
            d_writer = csv.DictWriter(output_csv_file, fieldnames=d_reader_b.fieldnames)
            d_writer.writeheader()

            final_output_rows = deduplicate(list_a, list_b)
            d_writer.writerows(final_output_rows)




def insert_title():
    with open("output.csv",'w') as output_csv_file:
        with open("cleaningdata.csv") as input_csv_file:
            d_reader = csv.DictReader(input_csv_file)

            d_reader.fieldnames = [field.strip().lower() for field in d_reader.fieldnames]

            output_field_names = generate_new_field_name(d_reader.fieldnames)

            # Prepare the output writer.
            d_writer = csv.DictWriter(output_csv_file, fieldnames=output_field_names)
            d_writer.writeheader()

            #start reading each row.
            for i, row in enumerate(d_reader):
                output_row_data = {}
                for output_field_name in output_field_names:
                    if output_field_name in row:
                        output_row_data[output_field_name] = row[output_field_name]
                current_title = "OTHER"
                doc = ""
                title_input = row["title"].lower()
                doc_input = row["standname"].lower()

                if any(c in title_input for c in ("ceo","chief executive officer")):
                    current_title = "CEO"
                elif any(c in title_input for c in ("cfo","chief financial officer")):
                    current_title = "CFO"
                elif any(c in title_input for c in ("coo","chief operating officer")):
                    current_title = "COO"
                elif any(c in title_input for c in ("cmo","chief marketing officer")):
                    current_title = "CMO"
                elif any(c in title_input for c in ("cno","chief nursing officer")):
                    current_title = "CNO"
                elif any(c in title_input for c in ("cio","chief information officer")):
                    current_title = "CIO"
                else: 
                    current_title = "OTHER"

                if doc_input.startswith(('dr ','dra.','dr.')) or doc_input.endswith(("md","md phd","do","d.o.","m.d.")) or any (c in title_input for c in ("physician","surgeon","surgery","dermatology","orthopedic","gastronenter","cardiologist","md","anesthesiologist","radiology")):
                    doc = "Y"



                output_row_data["title2"] = current_title
                output_row_data["doc"] = doc
                d_writer.writerow(output_row_data)

def generate_new_field_name(old_fieldnames):
    output_field_names = [old_fieldnames[0]]
    output_field_names.append("title2")
    output_field_names.append("doc")
    output_field_names.extend(old_fieldnames[1:])
    return (output_field_names)

def deduplicate(table_a,table_b):
    index_a = 0
    index_b = 0
    new_output = []
    while index_a < len(table_a) and index_b < len(table_b):
        current_row = table_b[index_b]
        compare_indicator = compare_table(table_a[index_a],current_row)
        if compare_indicator == 0:
            index_b += 1
            index_a += 1
            new_output.append(current_row)  
        elif compare_indicator > 0:
            index_b += 1
        else:
            index_a += 1
    for x in new_output:
        table_b.remove(x)
    return table_b

def compare_table(row_a,row_b):
    if (row_a["FYE"] < row_b["fye"]):
        return -1
    elif row_a["FYE"] == row_b["fye"]:
        if row_a["StandNAME"] < row_b["standname"]:
            return -1
        elif row_a["StandNAME"] == row_b["standname"]:
            if row_a["Total_Comp"] < row_b["totalcomp"]:
                return -1
            elif row_a["Total_Comp"] == row_b["totalcomp"]:
                return 0
            else:
                return 1
        else:
            return 1
    else:
        return 1

# Main
output_dup_rows()