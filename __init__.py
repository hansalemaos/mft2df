import os
import subprocess
import io
import tempfile
import pandas as pd
import re
from getfilenuitkapython import get_filepath
import gc

createdump = get_filepath("mft.exe")
parasedump = get_filepath("mft_dump.exe")

startupinfo = subprocess.STARTUPINFO()
startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
startupinfo.wShowWindow = subprocess.SW_HIDE
creationflags = subprocess.CREATE_NO_WINDOW
invisibledict = {
    "startupinfo": startupinfo,
    "creationflags": creationflags,
    "start_new_session": True,
}


def get_tmpfile(suffix: str = ".pqt") -> str:
    r"""
    Returns a temporary file path with the specified suffix.

    Args:
        suffix (str): The suffix for the temporary file. Default is ".pmc".

    Returns:
        str: The path to the temporary file.
    """
    tfp = tempfile.NamedTemporaryFile(delete=True, suffix=suffix)
    filename = os.path.normpath(tfp.name)
    tfp.close()
    return filename


def list_files_from_drive(drive: str = "c", convert_dates: bool = True) -> pd.DataFrame:
    """
    Retrieves a list of files from a specified drive and returns the results as a pandas DataFrame.

    Args:
        drive (str): The drive letter to retrieve the files from. Default is "c".
        convert_dates (bool): Whether to use pd.to_datetime to convert "FileNameLastModified", "FileNameLastAccess",
                               "FileNameCreated","StandardInfoLastModified","StandardInfoLastAccess","StandardInfoCreated"
                              (Parsing takes about 2x longer, and the resulting DataFrame is about 30% bigger)

    Returns:
        pd.DataFrame: A DataFrame containing the list of files retrieved from the drive.

    Raises:
        None
    """
    drive_re = re.findall(r"[a-z]+", drive, flags=re.I)[0].lower()
    mfttmpfile = get_tmpfile(".file")
    dumpcommand = [createdump, "dump", drive_re, f"{mfttmpfile}"]
    parsecommand = [parasedump, "-o", "csv", mfttmpfile]
    _ = subprocess.run(dumpcommand, capture_output=True, **invisibledict)
    opu = subprocess.run(parsecommand, capture_output=True, **invisibledict)
    tmpstring = io.StringIO(opu.stdout.decode("utf-8"))
    del opu
    del _
    gc.collect()
    df = pd.read_csv(
        tmpstring,
        sep=",",
        header=0,
        true_values=["true"],
        false_values=["false"],
        skip_blank_lines=True,
        on_bad_lines="warn",
        names=[
            "Signature",
            "EntryId",
            "Sequence",
            "BaseEntryId",
            "BaseEntrySequence",
            "HardLinkCount",
            "Flags",
            "UsedEntrySize",
            "TotalEntrySize",
            "FileSize",
            "IsADirectory",
            "IsDeleted",
            "HasAlternateDataStreams",
            "StandardInfoFlags",
            "StandardInfoLastModified",
            "StandardInfoLastAccess",
            "StandardInfoCreated",
            "FileNameFlags",
            "FileNameLastModified",
            "FileNameLastAccess",
            "FileNameCreated",
            "FullPath",
        ],
        dtype={
            "Signature": "category",
            "EntryId": "uint32",
            "Sequence": "uint16",
            "BaseEntryId": "uint32",
            "BaseEntrySequence": "uint16",
            "HardLinkCount": "uint16",
            "Flags": "category",
            "UsedEntrySize": "uint16",
            "TotalEntrySize": "uint16",
            "FileSize": "uint64",
            "IsADirectory": "bool",
            "IsDeleted": "bool",
            "HasAlternateDataStreams": "bool",
            "StandardInfoFlags": "category",
            "StandardInfoLastModified": "string",
            "StandardInfoLastAccess": "string",
            "StandardInfoCreated": "string",
            "FileNameFlags": "category",
            "FileNameLastModified": "string",
            "FileNameLastAccess": "string",
            "FileNameCreated": "string",
            "FullPath": "string",
        },
        engine="c",
        low_memory=True,
    )

    df = df.dropna(subset="FullPath")
    gc.collect()
    df.loc[df.index, "FullPath"] = f"{drive_re}:\\" + df.FullPath
    df = df.reset_index(drop=True)
    gc.collect()
    if convert_dates:
        dateformat = "%Y-%m-%dT%H:%M:%S.%fZ"
        datecols = [
            "FileNameLastModified",
            "FileNameLastAccess",
            "FileNameCreated",
            "StandardInfoLastModified",
            "StandardInfoLastAccess",
            "StandardInfoCreated",
        ]
        for datecol in datecols:
            df[datecol] = pd.to_datetime(
                df[datecol], errors="coerce", format=dateformat
            )
            gc.collect()
    try:
        os.remove(mfttmpfile)
    except Exception as fe:
        print(fe)
    return df
