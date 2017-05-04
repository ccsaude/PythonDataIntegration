import tarfile
import logging
import os
import shutil


def decompressfile(filename, outdir, destdir):
    if tarfile.is_tarfile(filename):
        try:
            t = tarfile.open(filename, 'r')
            for member in t.getmembers():
                if os.path.splitext(member.name)[1] == ".sql":
                    t.extract(member, outdir)
                    finalise_extraction(outdir, destdir)

        except tarfile.ReadError:
            logging.debug("tarfile   module or is somehow  invalid/ file is opened")
        except tarfile.CompressionError:
            logging.debug(" when the backups cannot be decoded properly")
        except tarfile.TarError:
            logging.debug("IOerror: File cant be extracted")
    else:
        logging.debug(filename + " is not an .tar file")

    return


def sql_files(members):
    for tarinfo in members:
        if os.path.splitext(tarinfo.name)[1] == ".sql":
            yield tarinfo


def finalise_extraction(outdir, dest_dir):
    # create temp dir to put the .sql file
    # os.mkdir(outdir + "/" + filename[:len(filename) - 4])
    for path, dirs, files in os.walk(outdir, topdown=True):
        for name in files:
            if name.endswith(".sql"):
                logging.info("moving file: " + name + " to sql_data_files dir")
                # Move the file to sql_data_files dir
                try:
                    shutil.move(src=os.path.join(path, name), dst=dest_dir)
                except shutil.Error as why:
                    print(str(why))
                    logging.debug(str(why))
