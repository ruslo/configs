" Copyright (c) 2013, Ruslan Baratov
" All rights reserved.

" Copy this file to ~/.vim/after/syntax/c.vim (unix)
" or <gvim-install-dir>/Vim/vimfiles/syntax/c.vim (windows)

" Highlight uint (add |typedef unsigned uint|)
syntax keyword cType uint

" Highlight some useful macro, prevent misprint
highlight userMacro ctermfg=darkyellow guifg=darkyellow

" Highlight tabs and spaces at end of line
syntax match cTodo "\t"
syntax match cTodo "\s\+$"

" Highlight __FUNCTION__ macro (see gcc)
syntax keyword cConstant __FUNCTION__
