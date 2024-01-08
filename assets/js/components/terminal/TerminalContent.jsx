import React, {forwardRef, Suspense, useEffect, useReducer, useRef, useState} from "react";
import {Terminal} from "@xterm/xterm";
import {FitAddon} from "@xterm/addon-fit";
import {WebglAddon} from "@xterm/addon-webgl";
import {useSocket} from "../SocketProvider";
import {AttachAddon} from "@xterm/addon-attach";



const TerminalContent = forwardRef(({children}, ref) => {
  const contentRef = useRef();
  const term = useRef({
    xterm: new Terminal({
      cursorBlink: true,
      convertEol: true,
      fontFamily: "JetBrains Mono",
    }),
    fitAddon: new FitAddon(),
    webglAddon: new WebglAddon(),
    attachAddon: null,
  });
  const {sendMessage, readyState, webSocketIns, connect, disconnect} = useSocket();


  React.useImperativeHandle(ref, () => ({
    ...contentRef,
    onResize,
  }));

  const onResize = () => {
    console.log('ONRESIZE', webSocketIns);
    term.current.fitAddon.fit();
    if (readyState === 1) {
      sendMessage(
        JSON.stringify([
          'resize',
          {
            cols: term.current.xterm.cols,
            rows: term.current.xterm.rows,
          },
        ])
      );
    }
  };

  useEffect(() => {
    connect()
    const elem = contentRef.current
    const xterm = term.current.xterm
    const fitAddon = term.current.fitAddon
    xterm.loadAddon(fitAddon)
    xterm.loadAddon(term.current.webglAddon)
    xterm.open(elem)
    fitAddon.fit()

    return () => onComponentUnmount()
  }, []);

  useEffect(() => {
    if (readyState === 1 && webSocketIns) {
      console.log(webSocketIns)
      const attAddon = term.current.attachAddon = new AttachAddon(webSocketIns)
      term.current.xterm.loadAddon(attAddon)

      webSocketIns.onclose = () => {
        console.log('SOCKET CONNECTION CLOSED')
        term.current.xterm.reset();
      }
      webSocketIns.onopen = () => {
        console.log('SOCKET CONNECTION OPENED')
      }
    }
  }, [readyState]);



  const onComponentUnmount = () => {
    console.log('TerminalContent UN-MOUNT');
    term.current.xterm.reset();
    disconnect();
  }

  return (
    <Suspense>
      <div ref={contentRef} className='term-content'>
        {children}
      </div>
    </Suspense>
  )
})


TerminalContent.displayName = 'TerminalContent'

export default TerminalContent