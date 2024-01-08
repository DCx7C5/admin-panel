import {RestrictedContent} from "./components/RestrictedContent";
import React, {lazy, useCallback, useEffect, useRef} from "react";
import DataProvider from "./components/DataProvider";
import {createPortal} from "react-dom";
const Terminal = lazy(
  () => import('./components/terminal/index'))
const TerminalToggleButton = lazy(
  () => import('./components/terminal/TerminalToggleButton'))


const Base = ({children}) => {
  const onclickRef = useRef(() => {})

  const toggleCb = useCallback((toggleFunc) => {
    onclickRef.current = toggleFunc
    console.log('lllllll',toggleFunc)
  }, [])

  return (
    <DataProvider dataElementId={'user-data'}>
      {children}
      <RestrictedContent>
        <Terminal toggleCb={toggleCb} />
        {createPortal
          (<TerminalToggleButton onClick={onclickRef}/>, document.body)
        }
      </RestrictedContent>
    </DataProvider>
  )
}

export default Base