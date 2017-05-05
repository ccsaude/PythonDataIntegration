import os
from filemanager import decompressfile
import logging

# Read config file
with open("/home/agnaldo/config.yaml", 'r') as stream:
    try:
        config = yaml.load(stream)

    except yaml.YAMLError as exc:
        logging.debug(str(exc))

basedir = config['basedir']
outdir = basedir + config['outdir']
backup_dir = basedir + config['backup_dir']
datadir = basedir + config['datadir']


# Logging
logfile = "/pylog.log"
logging.basicConfig(filename=outdir + logfile, format='%(asctime)s %(levelname)s:%(message)s', level=logging.DEBUG)

if os.path.isdir(basedir):

    logging.info("changing dir to : " + backup_dir)
    os.chdir(backup_dir)

    for path, dirs, files in os.walk('.', topdown=True):
        i = 0
        for name in files:
            if name.endswith(".tar"):
                # Untar all backupfiles
                i += 1
                logging.info("File found: " + name)
                decompressfile(name, outdir, datadir)
        if i == 0:
            logging.info("No backup file was found:")
else:
    logging.debug("IOerror: path was not found")