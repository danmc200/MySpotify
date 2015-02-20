let g:action=""

function! MySpotify()

let strUn=input('Enter username: ')
let strPwd=input('Enter password: ')

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
endfunction

function! Quit()
    let g:action="quit"
endfunction

function! Search()
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

au WinLeave * silent call Quit()
au VimLeave * silent call Quit()
