def unzip_content(content_type, file_name, content_name):

    # Rename the file to .zip
    base = os.path.splitext(file_name)[0]
    os.rename(file_name, base + ".zip")
    zip_file_name = file_path + content_name + ".zip"

    #Extract zip file
    zip_ref = zipfile.ZipFile(zip_file_name,'r')
    #Location where extracted files will go
    if content_type == 'workbook':
        zip_ref.extractall(file_path+"Extracted Workbooks")
        zip_ref.close()
        print "Extract of .twb file complete\n"

        #Delete everything that's not the .twb file
        for f in os.listdir(file_path+"Extracted Workbooks"):
            if os.path.isdir(file_path+"Extracted Workbooks/"+f):
                shutil.rmtree(file_path+"Extracted Workbooks/"+f)
            elif not f.endswith('.twb'):
                os.remove(file_path+"Extracted Workbooks/"+f)
        print "Workbook cleanup complete\n"
        new_file = base.replace(download_path,'')+".twb"

    elif content_type == 'datasource':
        zip_ref.extractall(file_path+"Extracted Datasources")
        zip_ref.close()
        print "Extract of .tds file complete\n"

        #Delete everything that's not the .tds file
        for f in os.listdir(file_path+"Extracted Datasources"):
            if os.path.isdir(file_path+"Extracted Datasources/"+f):
                shutil.rmtree(file_path+"Extracted Datasources/"+f)
            elif not f.endswith('.tds'):
                os.remove(file_path+"Extracted Datasources/"+f)
        print "Datasource cleanup complete\n"
        new_file = base.replace(download_path,'')+".tds"

    #Delete the zip file
    os.remove(zip_file_name)
    print "File "+zip_file_name+" removed\n"
    return new_file
