# configs

## Python scripts

### trash.py
Wrapper for `rm` command. Idea is usual - do not remove file, but move it to trash directory, restore it later, if needed.
Very useful in scripts, when you don't want to remove files that may be important and don't want to stop
script and ask user about deletion. [Read more](https://github.com/ruslo/configs/wiki/trash.py-usage)

### unpack.py
Wrapper for `unzip`, `gzip`, `tar`, ... Detect type of a file by extension and unpack it.
[Read more](https://github.com/ruslo/configs/wiki/unpack.py-usage)

### gvim.py
Wrapper/switcher for `gvim`/`vim` command. Sometimes it's tricky to start gvim (for example:
start windows gvim from cygwin, MacVim from mac os), sometimes you don't have gvim at all and want to use vim
(for example on server with console-mode only). This script wrap all this job.
[Read more](https://github.com/ruslo/configs/wiki/gvim.py-usage)

## Configs
One more collection of dotfiles (vim, git, bashrc, ...) with easy integration, just run `setup.py`.

## Setup
* Read more about [setup.py](https://github.com/ruslo/configs/wiki/setup.py-usage)
* Read more about [gitenv](https://github.com/ruslo/gitenv)

### Integration with gitenv
```bash
> git clone https://github.com/ruslo/gitenv
Cloning into 'gitenv'...
...
# Init configs submodule
> cd gitenv/ && git submodule init configs
Submodule 'configs' (...) registered ...
> git submodule update
Cloning into 'configs'...
# Run setup
> ./configs/setup.py --gitenv-root `pwd`
Init: /.../c.vim -> /.../.vim/after/syntax/c.vim
...
# reload configuration
> source ~/.bashrc
# test some script
> touch x && trash.py x
trash: 'x'
    -> '/.../.trash-data/2013/10-October/18-Friday/x-tfsfbj'
```

### Configs + python scripts
```bash
> git clone https://github.com/ruslo/configs
Cloning into 'configs'...
...
# Run setup
> ./configs/setup.py
Init: /.../configs/unix/bashrc.temp -> /.../.bashrc
Init: /.../vim/c.vim -> /.../.vim/after/syntax/c.vim
...
# reload configuration
> source ~/.bashrc
# test some script
> touch x && trash.py x
trash: 'x'
    -> '/.../.trash-data/2013/10-October/18-Friday/x-tfsfbj'
```

### Just python scripts
```bash
> git clone https://github.com/ruslo/configs
Cloning into 'configs'...
...
# Add python directory to PATH (do not forget export!)
> export PATH=`pwd`/configs/python:${PATH}
# test some script
> touch x && trash.py x
trash: 'x'
    -> '/.../.trash-data/2013/10-October/18-Friday/x-tfsfbj'
```
