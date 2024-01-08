import React, {useEffect, useRef} from "react";
import useMoveElementVertical from "../../hooks/useMoveElementVertical";


const TerminalToggleButton = ({ onClick }) => {
  const elementRef = useRef();
  const [top, onMouseDown, onMouseClick] = useMoveElementVertical(
    elementRef,
    'vertical',
    onClick.current,
    60
  );

  return (
    <div id='terminal-toggle'>
      <i ref={elementRef}
         onMouseDown={onMouseDown}
         onClick={onMouseClick}
         id='terminal-toggle-btn'
         className='bi bi-terminal'
         style={{top: top + 'px'}}
      />
    </div>
  )
};

export default TerminalToggleButton;
