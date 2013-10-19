" Copyright (c) 2013, Ruslan Baratov
" All rights reserved.

" This is special scheme to view man pages

set filetype=man
set nolist
set nonumber

" disable margin
let &colorcolumn=join(range(999,999),",")

if has("gui_running")
  " get maximum width
  set columns=999
endif
