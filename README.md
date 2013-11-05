# configs
| standalone  | gitenv |
|-------------|--------|
| [![][link_build_configs_master]][link_build_configs_branches] | [![][link_build_gitenv_master]][link_build_gitenv_branches] |

[link_build_configs_master]: https://travis-ci.org/ruslo/configs.png?branch=master
[link_build_configs_branches]: https://travis-ci.org/ruslo/configs/branches
[link_build_gitenv_master]: https://travis-ci.org/ruslo/gitenv.png?branch=master
[link_build_gitenv_branches]: https://travis-ci.org/ruslo/gitenv/branches

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

### open.py
Open files by extensions. Use programs which is listed in configuration file `~/.open.py`.
[Read more](https://github.com/ruslo/configs/wiki/open.py-usage)

## Configs
One more collection of dotfiles (vim, git, bashrc, ...) with easy integration, just run `setup.py`.

## Setup
* Read more about [setup.py](https://github.com/ruslo/configs/wiki/setup.py-usage)
* Read more about [gitenv](https://github.com/ruslo/gitenv)

### Integration with gitenv
```bash
> git clone https://github.com/ruslo/gitenv
> cd gitenv/ && git submodule init configs
> git submodule update
> ./configs/setup.py --gitenv-root `pwd`
> source ~/.bashrc # Reload configuration
# Now test new environment
> touch x && trash.py x
trash: 'x'
    -> '/.../.trash-data/2013/10-October/18-Friday/x-tfsfbj'
```

### Configs + python scripts
```bash
> git clone https://github.com/ruslo/configs
> ./configs/setup.py
> source ~/.bashrc # Reload configuration
# Now test new environment
> touch x && trash.py x
trash: 'x'
    -> '/.../.trash-data/2013/10-October/18-Friday/x-tfsfbj'
```

### Just python scripts
```bash
> git clone https://github.com/ruslo/configs
# Add python directory to PATH (do not forget export!)
> export PATH=`pwd`/configs/python:${PATH}
# Now test new environment
> touch x && trash.py x
trash: 'x'
    -> '/.../.trash-data/2013/10-October/18-Friday/x-tfsfbj'
```
