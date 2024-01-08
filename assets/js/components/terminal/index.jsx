import '../../../css/terminal.scss';
import React, {lazy, Suspense, useCallback, useEffect, useRef} from "react";
import useHideElement from "../../hooks/useHideElement";
import TerminalTaskbar from "./TerminalTaskbar";
import TerminalContent from "./TerminalContent";
import SocketProvider from "../SocketProvider";

const TerminalContainer = lazy(
    () => import('./TerminalContainer'))


const Terminal = ({toggleCb}) => {
  const contentRef = useRef();
  const [isVisible,,, toggleTerminal] = useHideElement(false,'term.show')
  const onContentResizeFunc = useRef();

  useEffect(() => {
    toggleCb(toggleTerminal);

    if (contentRef.current) {
      onContentResizeFunc.current = contentRef.current['onResize'];
    }
  }, [toggleCb, toggleTerminal]);

  const handleResize = useCallback(() => {
    if (onContentResizeFunc.current) {
      onContentResizeFunc.current();
      console.log('FIRED');
    }
  }, []);

  return (
    <SocketProvider endPoint='terminal'>
      <Suspense>
        {isVisible &&
          <TerminalContainer heightCallback={handleResize} >
            <TerminalTaskbar position='left' />
            <TerminalContent ref={contentRef} />
            <TerminalTaskbar position='right' />
          </TerminalContainer>
        }
      </Suspense>
    </SocketProvider>
  )
}

export default Terminal