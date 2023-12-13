import '../css/Terminal.css';
import 'xterm/css/xterm.css';
import $ from "jquery";
import 'jquery-ui';
import Split from 'split.js';
import React, {Component, Fragment} from 'react';
import { Terminal } from '@xterm/xterm';
import { FitAddon } from '@xterm/addon-fit';
import { AttachAddon } from "@xterm/addon-attach";

const splitter = Split(['#content', '#terminal-wrapper'], {
  direction: 'vertical',
  minSize: 0,
  onDragEnd(sizes) {
    localStorage.setItem('term.size', JSON.stringify(sizes))
  }
});

$("#nav-term-btn").click(function () {
  // Combine the selector for both .gutter and #terminal-wrapper
  const gutterAndTerminal = $(".gutter, #terminal-wrapper");
  // Check if both .gutter and #terminal-wrapper are visible
  const areBothVisible = gutterAndTerminal.is(":visible");
  gutterAndTerminal.toggle();
  // Save the visibility status in localStorage
  void localStorage.setItem("term.show", (!areBothVisible).toString());
});

// Load the visibility status from localStorage when the page loads
$(document).ready(async function () {
  const storedVisibility = localStorage.getItem("term.show");
  if (storedVisibility !== null) {
    const isVisible = storedVisibility === "true";
    $(".gutter, #terminal-wrapper").toggle(isVisible);
  }
  // Load the split sizes from localStorage or set default sizes
  const storedSize = localStorage.getItem("term.size");
  if (storedSize !== null) {
    let sizes = JSON.parse(storedSize);
    splitter.setSizes(sizes);
  } else {
    // Set default sizes if not found in localStorage
    let sizes = [100, 0];
    splitter.setSizes(sizes);
  }

});


export default class TerminalManager extends Component {
  constructor(props) {
    super(props);

    this.state = {
      userName: '',
      messageHistory: [],

    }
    this.socketUrl = 'ws://127.0.0.1:8000/ws/terminal/'
    this.socket = new WebSocket(this.socketUrl);
    this.terminal = new Terminal();
    this.fitAddon = new FitAddon();
    this.attachws = new AttachAddon(this.socket);
    this.terminal.loadAddon(this.fitAddon);
    this.terminal.loadAddon(this.attachws);

    this.wrapper = null;
    this.resizeObserver = null;


  }

  async componentDidMount() {
    console.log(this.terminal.onResize());
    this.terminal.open(this.element);
    this.fitAddon.fit();
    this.wrapper = document.getElementById('terminal-wrapper');
    this.resizeObserver = new ResizeObserver(this.onResize);
    if (this.wrapper) {
      this.resizeObserver.observe(this.wrapper);
    }
  }
  async componentWillUnmount() {
    if (this.resizeObserver) {
      this.resizeObserver.disconnect();
    }
  }

  onResize = () => {
    // Call fit method when the external div is resized
    this.fitAddon.fit();
  };

  render() {
    return (
      <>
        <div id="terminal-taskbar"></div>
        <div id="terminal-output"
             ref={(ref) => (this.element = ref)}>
        </div>
      </>
    );
  }
}
