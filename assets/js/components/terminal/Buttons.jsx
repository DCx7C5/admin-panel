import React, {useState} from "react";
import {useSocket} from "../SocketProvider";


export const StartStopButton = ({classes}) => {
  const [isPlayButton, setIsPlayButton] = useState(true);
  const { connect, disconnect } = useSocket();

  const handleClick = () => {
    isPlayButton ? connect() : disconnect()
    setIsPlayButton(!isPlayButton);
  };

  const color = isPlayButton ? {color: 'green'} : {color: 'red'}

  return (
    <button id="start-btn" className={"tb-btn btn " + classes} onClick={handleClick}>
      <i className={`bi bi-${isPlayButton ? 'play' : 'pause'}-fill`} style={color}></i> {isPlayButton ? 'Start' : 'Pause'}
    </button>
  );
};
