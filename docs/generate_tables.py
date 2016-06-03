import os
import re
import rst
from sqlalchemy import MetaData

import lsst.sims.ocs.database.tables as tbls

TOP_LEVEL_DIR = "docs"
GENERATED_TABLE_DIR = "tables"

def main():
    table_rst_files = []
    table_descr_match = re.compile(r'(?<=Description:).*?(?=Parameters)')

    if not os.path.exists(GENERATED_TABLE_DIR):
        os.mkdir(GENERATED_TABLE_DIR)

    create_calls = [k for k in dir(tbls) if "create" in k]
    for create_call in create_calls:
        func = getattr(tbls, create_call)
        if "session" in create_call:
            table = func(MetaData(), False)
        else:
            table = func(MetaData())

        table_name = table.fullname

        doc = rst.Document(table_name)

        # Get the table descriptions
        table_doc = " ".join([l.strip() for l in func.func_doc.split(os.linesep)])
        try:
            table_descr = table_descr_match.findall(table_doc)[0].strip()
        except IndexError:
            table_descr = ""
        para = rst.Paragraph(table_descr)
        doc.add_child(para)

        # Create table's column descriptions
        dtbl = rst.Table(header=["Column", "Description"])
        for column in table.columns.values():
            dtbl.add_item((column.name, column.doc))

        doc.add_child(dtbl)
        table_rst_file = os.path.join(GENERATED_TABLE_DIR, table_name.lower() + ".rst")
        doc.save(os.path.join(TOP_LEVEL_DIR, table_rst_file))
        table_rst_files.append(table_rst_file)

    collection_doc = rst.Document('Database Tables')
    para = rst.Paragraph(os.linesep.join([".. toctree::", "   :maxdepth: 2"]))
    collection_doc.add_child(para)
    for rst_file in table_rst_files:
        para = rst.Paragraph("   {}".format(rst_file.split(".rst")[0]))
        collection_doc.add_child(para)
    collection_doc.save(os.path.join(TOP_LEVEL_DIR, "table_descriptions.rst"))

if __name__ == "__main__":
    main()
