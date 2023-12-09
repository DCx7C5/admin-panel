import { Terminal } from "xterm";
import { FitAddon } from "xterm-addon-fit";
import WebSocket from 'ws';
import $ from 'jquery';

const term_out_elem = document.getElementById('terminal-output');
const term_container = document.getElementById('terminal-container');
const term = new Terminal({
    cursorBlink: true,
});
const fitAddon= new FitAddon();
const socket = new WebSocket('ws://' + window.location.host + '/term/')

function saveStateStorage() {

}

function loadStateStorage() {

}

function initTerminal() {
    term.loadAddon(fitAddon);
    term.open(term_out_elem);
    fitAddon.fit();
}

function resizeTerminal() {
    fitAddon.fit()
    socket.emit('')
}

export { WebSocket, initTerminal, resizeTerminal };