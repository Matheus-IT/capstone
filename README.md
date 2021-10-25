# Capstone

The final project of CS50W (Python and Javascript)

## Installation

\* Obs: Python version used in this project: 3.9.1

<details>
<summary style="cursor: pointer">Linux:</summary>
In the root directory of the project, you can create a virtual environment using  <code>python3 -m venv venv</code> , then running <code>source venv/bin/activate</code> will activate the virtual environment. To install all the dependencies this project requires run <code>pip3 install -r requirements.txt</code>, you should see a message saying that everything was installed.
</details>

<details>
<summary style="cursor: pointer">Windows:</summary>
In the root directory of the project, you can create a virtual environment using  <code>python3 -m venv venv</code>, then running <code>venv\Scripts\activate.bat</code> will activate the virtual environment. To install all the dependencies this project requires run <code>pip install -r requirements.txt</code>, you should see a message saying that everything was installed.

---

> **Notice**:
> In my experience on windows, when I ran `pip install -r requirements.txt` I got an error that said at the bottom:

```
ERROR: Command errored out with exit status 1: 'c:\users\mathe\documents\my django projects\capstone\venv\scripts\python.exe' -u -c 'import sys, setuptools, tokenize;
sys.argv[0] = '"'"'C:\\Users\\mathe\\AppData\\Local\\Temp\\pip-install-fljag7l5\\twisted_1cbe426cceda4bfca6c98c224e54b0d1\\setup.py'"'"'; __file__='"'"'C:\\Users\\mathe
\\AppData\\Local\\Temp\\pip-install-fljag7l5\\twisted_1cbe426cceda4bfca6c98c224e54b0d1\\setup.py'"'"';f=getattr(tokenize, '"'"'open'"'"',
open)(__file__);code=f.read().replace('"'"'\r\n'"'"', '"'"'\n'"'"');f.close();exec(compile(code, __file__, '"'"'exec'"'"'))' install --record 'C:\Users\mathe\AppData
\Local\Temp\pip-record-a08vaq1a\install-record.txt' --single-version-externally-managed --compile --install-headers 'c:\users\mathe\documents\my django projects\capstone
\venv\include\site\python3.9\Twisted' Check the logs for full command output.
```

To fix this I went to [This site](https://www.lfd.uci.edu/~gohlke/pythonlibs/#twisted) and downloaded this file
`Twisted-20.3.0-cp39-cp39-win_amd64.whl`, where "cp39" corresponds to the python version. After that I ran
`pip install path/to/file/Twisted-20.3.0-cp39-cp39-win_amd64.whl` and it installed this dependency successfully.
And then I tried again `pip install -r requirements.txt`, the installation was complete.

</details>

<details>
<summary style="cursor: pointer">Mac</summary>
I couldn't test on Mac OS, but the steps might be the same as the ones for <strong>linux</strong>.
</details>
