let g:action=""
let g:query=""

map <C-n> :call PlayNext() <CR>
map <C-p> :call PlayPrev() <CR>
map <Space> :call Pause() <CR>
noremap / :call Search() <CR>
set hls
set number

let strUn=input('Enter username: ')
let strPwd=input('Enter password: ')
: vsplit albums
: vsplit tracks

python << EOF

import vim, spotify
import run_my_spotify, vim_ui
import core.audio_player as audio_player

session = run_my_spotify.get_session()
ui = vim_ui.VimUI(vim)
player = audio_player.AudioPlayer(session, ui)
ui.init_ui(player)

un = vim.eval("strUn")
pwd = vim.eval("strPwd")
run_my_spotify.login(session, un, pwd)

EOF

function! Quit()
    let g:action="quit"
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

au VimLeave * silent call Quit()
