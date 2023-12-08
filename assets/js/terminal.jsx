import { Terminal } from "xterm";
import { FitAddon } from "xterm-addon-fit";
import '../css/terminal.css';

const term_elem = document.getElementById('terminal')
const terminal = new Terminal()
const fit= new FitAddon()

terminal.loadAddon(fit)
terminal.open(term_elem)
fit.fit()
