import os
from filemanager import decompressfile
import logging
import yaml
# import pymysql # uses a c extension to connect to mysql
import MySQLdb  # pure python library

# Read config file
with open("/home/agnaldo/config.yaml", 'r') as stream:
    try:
        config = yaml.load(stream)

    except yaml.YAMLError as exc:
        logging.debug(str(exc))
    else:
        basedir = config['basedir']
        outdir = basedir + config['outdir']
        backup_dir = basedir + config['backup_dir']
        datadir = basedir + config['datadir']


# Misc Functions
def mysqlgetconnection(usr, pwd):
    # Connect to the database
    conn = MySQLdb.connect(passwd=pwd, db=usr)
    return conn


def renamebackupfiles(sql_files_dir):
    if os.path.isdir(sql_files_dir):
        os.chdir(sql_files_dir)
        for root, dirs, files in os.walk('.', topdown=True):
            for f in files:
                if f.endswith(".sql"):
                    new_name = matchfacilityname(f)
                    # Alguns nomes nao serao encontrados na lista
                    # casos em que se escreve mal o nome da US no script de backup
                    # nestes casos deve-se corrigir o nome no script de backup (ex: Malhagalene -> Malhangalene)
                    if new_name != '':
                        os.rename(f, 'cs_' + new_name + '.sql')
                    else:
                        print(
                            f + " Nao iguala-se com algum nome na lista das US. Verifique se o nome do ficheiro esta correcto")
                        logging.debug(
                            f + " Nao iguala-se com algum nome na lista das US. Verifique se o nome do ficheiro esta correcto")
    return


def matchfacilityname(f_name):
    arr_facilities = config['facilities']
    facility = ''
    for f in arr_facilities:
        if f.lower() in f_name.lower():
            facility = f
            break
    return facility


if os.path.isdir(basedir):

    # log files
    logfile = "/pylog.log"
    logging.basicConfig(filename=outdir + logfile, format='%(asctime)s %(levelname)s:%(message)s',
                        level=logging.DEBUG)
    if os.path.isdir(backup_dir):
        logging.info("changing dir to : " + backup_dir)
        print("changing dir to : " + backup_dir)
        os.chdir(backup_dir)

        for path, dirs, files in os.walk('.', topdown=True):
            numtarfiles = 0
            for name in files:
                if name.endswith(".tar"):
                    # Untar all backupfiles
                    numtarfiles += 1
                    logging.info("File found: " + name)
                    print("File found: " + name)
                    decompressfile(name, outdir, datadir)
        if numtarfiles == 0:
            logging.info("No backup file was found:")
        else:
            print("Renaming sql_files in " + datadir)
            renamebackupfiles(datadir)

    else:
        logging.debug("IOerror: path " + backup_dir + " was not found")
        print("IOerror: path " + backup_dir + " was not found")
else:
    logging.debug("IOerror: path " + basedir + " was not found")
    print("IOerror: path " + basedir + " was not found")


def beginmysqljob(extracted_files, sql_files_dir):
    if os.path.isdir(sql_files_dir):
        os.chdir(sql_files_dir)
        sqlfiles = 0

        for path, dirs, files in os.walk('.', topdown=True):
            for n in files:
                if n.endswith(".sql"):
                    sqlfiles += 1
        if sqlfiles == 0:
            logging.info("No backup file extracted. check if you have backup files in the backup folder ")
            print("No backup file extracted. check if you have backup files in the backup folder ")
        elif sqlfiles == extracted_files and sqlfiles > 0:
            logging.info("Execution ok, starting mysql jobs...")
            print("Execution ok, starting mysql jobs...")
            # TODO - start mysql jobs here

        elif sqlfiles != extracted_files:
            logging.info("Some backup files (tar) were not extracted, check the logs for more details")
            print("Info: Some backup files (tar) were not extracted, check the logs for more details")
            print("starting mysql jobs...")
            # TODO - start mysql jobs here

    else:
        logging.debug("IOerror: path " + sql_files_dir + " was not found")
        print("IOerror: path " + sql_files_dir + " was not found")
