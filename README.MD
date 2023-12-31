# Lists the files on a drive insanely fast (43 seconds for 1,800,000 files - 600 GB) by converting the $MFT to a pandas DataFrame 

## pip install mft2df

### Tested against Windows 10 / Python 3.10 / Anaconda 


The list_files_from_drive function can be used by individuals or developers who need to retrieve a 
list of files from a specified drive. 
It can be particularly useful for tasks such as file system analysis, data exploration, or building file management utilities.

### Advantages of list_files_from_drive:

- Retrieves file information from the specified drive and returns it as a structured pandas DataFrame, allowing for easy data manipulation and analysis.
- Supports parsing of the Master File Table (MFT) dump using external utilities (mft.exe https://github.com/makitos666/MFT_Fast_Transcoder -to copy the mft-  and mft_dump.exe https://github.com/omerbenamram/mft -to parse the mft-) to extract file metadata.
- Uses subprocess calls to execute external commands in a hidden window, providing a seamless user experience.
- Parses the output of the MFT dump into a DataFrame using pandas, enabling efficient data handling and processing.
- Performs data type conversions and date parsing for specific columns, ensuring data consistency and usability.
- Filters out rows with missing FullPath values to ensure the integrity of the data.
- Prepends the drive letter to the FullPath column to create a complete file path.
- Cleans up the temporary MFT dump file after processing.
- Utilizes efficient memory management by explicitly deleting variables, garbage collection, and low-memory options in the pandas read_csv function.


```python
Args:
    drive (str): The drive letter to retrieve the files from. Default is "c".
    convert_dates (bool): Whether to use pd.to_datetime to convert "FileNameLastModified", "FileNameLastAccess",
                           "FileNameCreated","StandardInfoLastModified","StandardInfoLastAccess","StandardInfoCreated"
                          (Parsing takes about 2x longer, and the resulting DataFrame is about 30% bigger)
Returns:
    pd.DataFrame: A DataFrame containing the list of files retrieved from the drive.
Raises:
    None
    
# Important: you need admin rights!!!!
from mft2df import list_files_from_drive
from time import perf_counter
start = perf_counter()
df=list_files_from_drive(drive= "c")
print(f'Time needed: {perf_counter() - start} for {len(df)} files')
print(df[200060:200066].to_string())

# Time needed: 43.62916430000041 for 1842450 files

#        Signature  EntryId  Sequence  BaseEntryId  BaseEntrySequence  HardLinkCount      Flags  UsedEntrySize  TotalEntrySize  FileSize  IsADirectory  IsDeleted  HasAlternateDataStreams StandardInfoFlags     StandardInfoLastModified       StandardInfoLastAccess          StandardInfoCreated           FileNameFlags         FileNameLastModified           FileNameLastAccess              FileNameCreated                                                                                                                     FullPath
# 200060      FILE   202514         1            0                  0              2  ALLOCATED            672            1024       211         False      False                    False           (empty)  2020-03-04T10:38:59.012552Z  2020-03-04T10:38:59.012552Z  2020-03-04T10:39:00.779040Z  FILE_ATTRIBUTE_ARCHIVE  2020-03-04T10:38:59.012552Z  2020-03-04T10:38:59.012552Z  2020-03-04T10:38:59.012552Z  c:\Windows\WinSxS\Manifests\amd64_bthmtpenum.inf-languagepack_31bf3856ad364e35_10.0.18362.1_de-de_710d1caf8aa9bb19.manifest
# 200061      FILE   202515         1            0                  0              2  ALLOCATED            664            1024       208         False      False                    False           (empty)  2020-03-04T10:38:59.022586Z  2020-03-04T10:38:59.022586Z  2020-03-04T10:39:00.779040Z  FILE_ATTRIBUTE_ARCHIVE  2020-03-04T10:38:59.022586Z  2020-03-04T10:38:59.022586Z  2020-03-04T10:38:59.022586Z       c:\Windows\WinSxS\Manifests\amd64_c_wpd.inf-languagepack_31bf3856ad364e35_10.0.18362.1_de-de_a4c4bcf7ec41f07e.manifest
# 200062      FILE   202516         1            0                  0              2  ALLOCATED            672            1024       207         False      False                    False           (empty)  2020-03-04T10:38:59.032170Z  2020-03-04T10:38:59.032170Z  2020-03-04T10:39:00.779040Z  FILE_ATTRIBUTE_ARCHIVE  2020-03-04T10:38:59.032170Z  2020-03-04T10:38:59.032170Z  2020-03-04T10:38:59.022586Z     c:\Windows\WinSxS\Manifests\amd64_wpdcomp.inf-languagepack_31bf3856ad364e35_10.0.18362.1_de-de_78d37c0df7225559.manifest
# 200063      FILE   202517         1            0                  0              2  ALLOCATED            664            1024       207         False      False                    False           (empty)  2020-03-04T10:38:59.032699Z  2020-03-04T10:38:59.032699Z  2020-03-04T10:39:00.794664Z  FILE_ATTRIBUTE_ARCHIVE  2020-03-04T10:38:59.032699Z  2020-03-04T10:38:59.032699Z  2020-03-04T10:38:59.032699Z       c:\Windows\WinSxS\Manifests\amd64_wpdfs.inf-languagepack_31bf3856ad364e35_10.0.18362.1_de-de_a09f098927b0c6b9.manifest
# 200064      FILE   202518         1            0                  0              2  ALLOCATED            664            1024       208         False      False                    False           (empty)  2020-03-04T10:38:59.042535Z  2020-03-04T10:38:59.042535Z  2020-03-04T10:39:00.794664Z  FILE_ATTRIBUTE_ARCHIVE  2020-03-04T10:38:59.042535Z  2020-03-04T10:38:59.042535Z  2020-03-04T10:38:59.032699Z      c:\Windows\WinSxS\Manifests\amd64_wpdmtp.inf-languagepack_31bf3856ad364e35_10.0.18362.1_de-de_13d74fb245acf719.manifest
# 200065      FILE   202519         1            0                  0              2  ALLOCATED            672            1024       211         False      False                    False           (empty)  2020-03-04T10:38:59.042535Z  2020-03-04T10:38:59.042535Z  2020-03-04T10:39:00.794664Z  FILE_ATTRIBUTE_ARCHIVE  2020-03-04T10:38:59.042535Z  2020-03-04T10:38:59.042535Z  2020-03-04T10:38:59.042535Z    c:\Windows\WinSxS\Manifests\amd64_wpdmtphw.inf-languagepack_31bf3856ad364e35_10.0.18362.1_de-de_52e461d8f91111b2.manifest

```

## Examples

### Finds all python files on your HDD that contain the string "ctypes" in less than 2 minutes

```python
import pandas as pd
from PrettyColorPrinter import add_printer # pip install PrettyColorPrinter
add_printer(1)
from mft2df import list_files_from_drive
from time import perf_counter

start = perf_counter()
df = list_files_from_drive(drive="c", convert_dates=False)
print(f"Time needed: {perf_counter() - start} " f"for {len(df)} files")


def get_content(file):
    try:
        with open(file, mode="r", encoding="utf-8") as f:
            data = f.read()

    except Exception:
        data = pd.NA
    return data


dffi = df.loc[
    (df.FullPath.str.endswith(".py")) & (~df.IsDeleted) & (~df.IsADirectory)
].copy()
dffi["FileContent"] = dffi.FullPath.apply(get_content)
dffi = dffi.loc[~dffi["FileContent"].isna()]
ctypesfiles = dffi.loc[dffi.FileContent.str.contains("ctypes")]
```
