import React, {createContext, useContext, useRef} from "react";
import {useWebSocket} from "ahooks";

const SocketContext = createContext(null);


export const useSocket = () => {
  return useContext(SocketContext);
};


export const SocketProvider = ({ endPoint, children, manual= true }) => {
  const counter = useRef(0)
  const proto = document.location.protocol === 'https' ? 'wss' : 'ws'
  const {
    latestMessage,
    sendMessage,
    disconnect,
    connect,
    readyState,
    webSocketIns
    } = useWebSocket(
        proto+'://'+window.location.host+'/ws/'+endPoint+'/pty'+counter.current+'/',
        {
        reconnectLimit: 10,
        reconnectInterval: 6,
        manual: manual,
        protocols: 'websocket',
    })

  return (
    <SocketContext.Provider value={{
      sendMessage,
      latestMessage,
      webSocketIns,
      connect,
      disconnect,
      readyState
    }}>
      {children}
    </SocketContext.Provider>
  )
};

export default SocketProvider