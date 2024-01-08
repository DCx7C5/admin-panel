import React, {forwardRef, useCallback, useEffect, useRef} from "react";
import useDragResizeHeight from "../../hooks/useDragResizeHeight";



export const TerminalContainer = ({ children, heightCallback = null }) => {
  const resizableRef = useRef();
  const resizerRef = useRef();
  const {height, onMouseDown} = useDragResizeHeight(
    resizableRef,
    () => heightCallback && heightCallback()
  );

  return (
    <>
      <div id='terminal-container' >
        <div className='slider' onMouseDown={onMouseDown} >
          <div ref={resizerRef} className="lip" />
        </div>
        <div ref={resizableRef} id='terminal-wrapper' style={{height: height + 'px'}}>
          {children}
        </div>
      </div>
    </>
  )
}

TerminalContainer.displayName = 'TerminalContainer'

export default TerminalContainer