import os
import re
import rst
import shutil
from sqlalchemy import MetaData

import lsst.sims.ocs.database.tables as tbls

TOP_LEVEL_DIR = "docs"
GENERATED_TABLE_DIR = "tables"

def main():
    table_rst_files = []
    table_descr_match = re.compile(r'(?<=Description:).*?(?=Parameters)')

    table_file_path = os.path.join(TOP_LEVEL_DIR, GENERATED_TABLE_DIR)

    if not os.path.exists(table_file_path):
        os.mkdir(table_file_path)

    create_calls = [k for k in dir(tbls) if "create" in k and "summary" not in k]
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

    # Handle summary table
    doc = create_summary_all_props_table()
    table_rst_file = os.path.join(GENERATED_TABLE_DIR, "summaryallprops.rst")
    doc.save(os.path.join(TOP_LEVEL_DIR, table_rst_file))
    table_rst_files.append(table_rst_file)

    table_rst_files.sort()

    collection_doc = rst.Document('Database Tables')
    para = rst.Paragraph(os.linesep.join([".. toctree::", "   :maxdepth: 2"]))
    collection_doc.add_child(para)
    for rst_file in table_rst_files:
        para = rst.Paragraph("   {}".format(rst_file.split(".rst")[0]))
        collection_doc.add_child(para)
    collection_doc.save(os.path.join(TOP_LEVEL_DIR, "table_descriptions.rst"))

    # Write link anchors at top of file.
    for rst_file in table_rst_files:
        rst_full_file = os.path.join(TOP_LEVEL_DIR, rst_file)
        tmp_file = rst_full_file + "_tmp"
        link_anchor = ".. _database-tables-{}:".format(os.path.basename(rst_file).split(".rst")[0])
        with open(tmp_file, 'w') as ofile:
            with open(rst_full_file, 'r') as ifile:
                ofile.write(link_anchor + os.linesep)
                ofile.write(os.linesep)
                for row in iter(ifile):
                    ofile.write(row)
        shutil.move(tmp_file, rst_full_file)

def create_summary_all_props_table():
    """Create documentation for SummaryAllProps table.
    """
    obshistory = tbls.create_observation_history(MetaData())
    oh_columns_1 = ['observationId', 'night', 'observationStartTime', 'observationStartMJD',
                    'observationStartLST', 'numExposures', 'visitTime', 'visitExposureTime']
    oh_columns_2 = ['fieldId', 'fieldRA', 'fieldDec', 'altitude', 'azimuth', 'filter', 'airmass',
                    'skyBrightness', 'cloud', 'seeingFwhm500', 'seeingFwhmGeom', 'seeingFwhmEff']
    oh_columns_3 = ['moonRA', 'moonDec', 'moonAlt', 'moonAz', 'moonDistance', 'moonPhase', 'sunAlt', 'sunAz',
                    'solarElong']

    obsprophist = tbls.create_observation_proposal_history(MetaData())
    oph_columns = ['Proposal_propId']
    oph_relabel = ['proposalId']

    slewhistory = tbls.create_slew_history(MetaData())
    sh_columns = ['slewTime', 'slewDistance']

    slewfinalstate = tbls.create_slew_final_state(MetaData())
    sfs_columns = ['paraAngle', 'rotTelPos', 'rotSkyPos']

    doc = rst.Document("SummaryAllProps")

    # Table description
    table_descr = ["This table contains a summary set of information from the observations by joining"]
    table_descr.append("certain columns from particular tables. There is one row for each proposal observed")
    table_descr.append("target. If more that one proposal received the same observation, rows with mostly ")
    table_descr.append("duplicated information, except proposal Id, are created.")
    para = rst.Paragraph(os.linesep.join(table_descr))
    doc.add_child(para)

    # Table columns
    dtbl = rst.Table(header=["Column", "Description"])
    filtered_column_documentation(dtbl, obshistory, oh_columns_1)
    filtered_column_documentation(dtbl, obsprophist, oph_columns, oph_relabel)
    filtered_column_documentation(dtbl, obshistory, oh_columns_2)
    filtered_column_documentation(dtbl, slewhistory, sh_columns)
    filtered_column_documentation(dtbl, slewfinalstate, sfs_columns)
    filtered_column_documentation(dtbl, obshistory, oh_columns_3)

    doc.add_child(dtbl)
    return doc

def filtered_column_documentation(dtbl, t, cfilter, clabel=None):
    """Generate column documentation with respect to a filter.
    """
    for c in t.columns.values():
        if c.name in cfilter:
            if clabel is not None:
                c_name = clabel.pop(0)
            else:
                c_name = c.name
            dtbl.add_item((c_name, c.doc))

if __name__ == "__main__":
    main()
