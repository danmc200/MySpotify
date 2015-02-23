let g:action=""
let g:query=""

map <Return> :call Select() <CR>
map <C-n> :call PlayNext() <CR>
map <C-p> :call PlayPrev() <CR>
map <Space> :call Pause() <CR>
noremap / :call Search() <CR>
map q :call Quit() <CR>
set hls
set number

let strUn=input('Enter username: ')
let strPwd=input('Enter password: ')

python << EOF

import vim, spotify
import core.login as login
import vim_ui
import core.audio_player as audio_player

session = login.get_session()
ui = vim_ui.VimUI(vim)
player = audio_player.AudioPlayer(session, ui)
ui.init_ui(player)

un = vim.eval("strUn")
pwd = vim.eval("strPwd")
login.login(session, un, pwd)

EOF

function! Quit()
    let quit=input('Quit? (y/n)')
    if quit =~ "y"
        let g:action="quit"
    endif
endfunction

function! Search()
    let g:query=input('Enter search: ')
    let g:action="search"
endfunction

function! PlayNext()
    let g:action="next"
endfunction

function! PlayPrev()
    let g:action="prev"
endfunction

function! Play()
    let g:action="play"
endfunction

function! Pause()
    let g:action="pause"
endfunction

function! Select()
    let g:action="select"
endfunction
