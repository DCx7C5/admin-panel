import React, { Children, useEffect, useState } from 'react';
import { useSocket } from "./SocketProvider";
import {ReadyState} from "ahooks/es/useWebSocket";


export const ConnectionStateIndicator = ({ }) => {
  const [text, setText] = useState('Closed');
  const [color, setColor] = useState({color: 'red'});
  const { readyState } = useSocket();

  useEffect(() => {
    setText(connectionStatus)
    if (readyState === 0) {
      setColor({color: 'orange'})
    } else if (readyState === 1) {
      setColor({color: 'green'})
    } else {
      setColor({color: 'red'})
    }

  }, [readyState]);

  const connectionStatus = {
    [ReadyState.Connecting]: 'Connecting',
    [ReadyState.Open]: 'Connected',
    [ReadyState.Closing]: 'Closing',
    [ReadyState.Closed]: 'Closed',
  }[readyState];

  return <a>
    <i style={color} className="bi bi-circle-fill"></i>
    <span className='conn-state-text'
          style={{
            color: 'white',
            fontFamily: "JetBrains Mono",
            fontWeight: 'bold',
          }}
    > {text}</span>
  </a>
}


export const TerminalTaskbar = ({children, connectionState}) => {

  useEffect(() => {


  }, [connectionState]);

  return <div id='terminal-taskbar' className='navbar navbar-expand-lg'>
    <div className='container-fluid d-flex justify-content-start'>
      {Children.map(children, (child, index) => (
        <div className={'nav-item nav-btn-wrapper'} key={index}>{child}</div>
      ))}
    </div>
  </div>
}
