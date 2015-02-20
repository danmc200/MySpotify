let g:quitSpot="false"

function! MySpotify()

let strUn=input('Enter username: ')
let strPwd=input('Enter password: ')

python << EOF

import vim, spotify
import run_my_spotify, vim_ui

session = spotify.Session()
ui = vim_ui.VimUI(vim)
player = run_my_spotify.AudioPlayer(session, ui)
ui.init_ui(player)

un = vim.eval("strUn")
pwd = vim.eval("strPwd")
run_my_spotify.login(session, un, pwd)
ui.do_search()

EOF
endfunction

function! Quit()
    let g:quitSpot="true"
endfunction

au WinLeave * silent call Quit()
au VimLeave * silent call Quit()
