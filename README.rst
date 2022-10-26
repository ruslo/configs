.. code-block:: none

  [configs]> echo "source `readlink -f unix/bashrc`" >> ~/.bashrc
  [configs]> cp unix/bash_profile ~/.bash_profile

.. code-block:: none

  [configs]> cp vim/vimrc ~/.vimrc
  [configs]> mkdir -p ~/.vim/after/syntax/
  [configs]> cp vim/c.vim ~/.vim/after/syntax/c.vim
  [configs]> cp vim/rst.vim ~/.vim/after/syntax/rst.vim
  [configs]> cp vim/man-scheme.vim ~/.vim/after/syntax/man-scheme.vim
  [configs]> cp vim/gitcommit.vim ~/.vim/after/syntax/gitcommit.vim

.. code-block:: none

  [configs]> mkdir -p ~/.config/git/
  [configs]> cp git/config ~/.gitconfig
  [configs]> cp git/attributes ~/.config/git/attributes
