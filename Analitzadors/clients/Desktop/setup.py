# python setup.py py2exe --includes sip

from distutils.core import setup
import py2exe
import matplotlib

setup(
     windows=['visor.py'],
     options={
              'py2exe': {
                         'packages' : ['matplotlib', 'pytz'],
                         "dll_excludes": ["libgdk_pixbuf-2.0-0.dll",
				          "libgobject-2.0-0.dll",
					  "libgdk-win32-2.0-0.dll"] ,
                        }
             },

     data_files=matplotlib.get_py2exe_datafiles(),
)

